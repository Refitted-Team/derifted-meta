import os, subprocess, sys
from datetime import date

currentDate = date.today()

# TODO: Remove, this is temp
os.environ["META_UPSTREAM_DIR"] = "upstream"
os.environ["META_UPSTREAM_URL"] = "https://github.com/Novampr/upstream-meta"
os.environ["META_LAUNCHER_DIR"] = "launcher"
os.environ["META_LAUNCHER_URL"] = "https://github.com/Novampr/launcher-meta"

def init_repo(directory, url, msg):
    if os.path.exists(directory):
        return True

    if url == None or url == "":
        print(f"Can't initialize missing ${directory} directory. Please specify ${msg}")
        return False

    subprocess.call(["git", "clone", url, directory])
    return True

if not init_repo(os.environ["META_UPSTREAM_DIR"], os.environ["META_UPSTREAM_URL"], "META_UPSTREAM_URL"):
    sys.exit(1)

if not init_repo(os.environ["META_LAUNCHER_DIR"], os.environ["META_LAUNCHER_URL"], "META_LAUNCHER_URL"):
    sys.exit(1)

def upstream_git(args):
    return subprocess.call(["git", "-C", os.environ["META_UPSTREAM_DIR"]] + args)

def launcher_git(args):
    return subprocess.call(["git", "-C", os.environ["META_LAUNCHER_DIR"]] + args)

upstream_git(["reset", "--hard", "HEAD"])

subprocess.call(["python", "-m", "meta.run.update_mojang"])
subprocess.call(["python", "-m", "meta.run.update_forge"])
subprocess.call(["python", "-m", "meta.run.update_neoforge"])
subprocess.call(["python", "-m", "meta.run.update_fabric"])
subprocess.call(["python", "-m", "meta.run.update_quilt"])

if os.environ["DEPLOY_TO_GIT"] == "true":
    upstream_git(["add", "mojang/version_manifest_v2.json", "mojang/java_all.json", "mojang/versions/*"])
    upstream_git(["add", "forge/*.json", "forge/version_manifests/*.json", "forge/installer_manifests/*.json", "forge/files_manifests/*.json", "forge/installer_info/*.json"])
    upstream_git(["add", "neoforge/*.json", "neoforge/version_manifests/*.json", "neoforge/installer_manifests/*.json", "neoforge/files_manifests/*.json", "neoforge/installer_info/*.json"])
    upstream_git(["add", "fabric/loader-installer-json/*.json", "fabric/meta-v2/*.json", "fabric/jars/*.json"])
    upstream_git(["add", "quilt/loader-installer-json/*.json", "quilt/meta-v3/*.json", "quilt/jars/*.json"])
    upstream_git(["add", "liteloader/*.json"])
    if upstream_git(["diff", "--cached", "--exit-code"]) == 1:
        upstream_git(["commit", "-a", "-m", f"Update ${currentDate}"])
        upstream_git(["push"])

subprocess.call(["python", "-m", "meta.run.generate_mojang"])
subprocess.call(["python", "-m", "meta.run.generate_forge"])
subprocess.call(["python", "-m", "meta.run.generate_neoforge"])
subprocess.call(["python", "-m", "meta.run.generate_fabric"])
subprocess.call(["python", "-m", "meta.run.generate_quilt"])
subprocess.call(["python", "-m", "meta.run.index"])

if os.environ["DEPLOY_TO_GIT"] == "true":
    launcher_git(["add", "index.json org.lwjgl/*", "org.lwjgl3/*", "net.minecraft/*"])
    launcher_git(["add", "net.minecraftforge/*"])
    launcher_git(["add", "net.neoforged/*"])
    launcher_git(["add", "net.fabricmc.fabric-loader/*", "net.fabricmc.intermediary/*"])
    launcher_git(["add", "org.quiltmc.quilt-loader/*"])
    if launcher_git(["diff", "--cached", "--exit-code"]) == 1:
        launcher_git(["commit", "-a", "-m", f"Update ${currentDate}"])
        launcher_git(["push"])