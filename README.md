# DevOps Laboratory Work 1 - Danil Marchenko

**Student:** Danil Marchenko  
**Group:** IT2-2303  
**Student ID:** 41587  
**Course:** DevOps  
**GitHub:** [jardemAI/DevOps](https://github.com/jardemAI/DevOps)

## Project layout

```text
marchenko-danil-devops/
├── app/                    # Python HTTP application
├── assets/                 # workflow diagram source and rendering
├── backup/                 # ignored runtime backup files
├── config/app.conf
├── logs/                   # runtime application.log is intentionally ignored
├── scripts/Marchenko_Danil_system.sh
├── tests/test_app.py
├── Dockerfile
├── Jenkinsfile
├── Lab_Report.md
├── Lab_Report.pdf
├── docker-compose.yml
├── Marchenko_Danil_info.txt
├── private.txt
└── public.txt
```

## Part A - Linux

The project is in `~/devops/marchenko-danil-devops`. Required directories are `app`, `scripts`, `config`, `logs`, and `backup`. `Marchenko_Danil_info.txt` contains the student details. `config/app.conf` documents non-secret settings. `logs/application.log` is a local ignored runtime log; `logs/application.log.example` is kept in Git.

Useful demonstrations from the project directory:

```bash
pwd
ls -la
cd ~/devops/marchenko-danil-devops
mkdir -p /tmp/devops-demo
touch /tmp/devops-demo/source.txt
cp /tmp/devops-demo/source.txt /tmp/devops-demo/copy.txt
mv /tmp/devops-demo/copy.txt /tmp/devops-demo/renamed.txt
cat Marchenko_Danil_info.txt
head -n 5 logs/application.log
tail -n 5 logs/application.log
rm -r /tmp/devops-demo
find . -name application.log
grep 'ERROR' logs/application.log
grep 'WARNING' logs/application.log
grep -c 'ERROR' logs/application.log
tail -n 5 logs/application.log
```

`pwd` prints the current path; `ls` lists entries; `cd` changes directory; `mkdir` creates directories; `touch` creates a file or updates its timestamp; `cp` copies; `mv` moves or renames; `rm` removes; `cat` prints file contents; `head` and `tail` print the first and last lines. `find` searches by path or name. `grep` selects matching lines and `grep -c` counts them. The sample log has 12 lines, 2 `ERROR` records, and 3 `WARNING` records.

Permissions differ by design: `private.txt` uses mode `600` (`rw-------`), so only its owner can read or write it; `public.txt` uses `644` (`rw-r--r--`), so the owner can read and write and everyone else can read. `r` means read, `w` means write, and `x` means execute for a file or directory traversal for a directory. The owner is the file's user, the group is its assigned group, and others are all remaining users. Git records the executable bit, not ordinary read/write differences, so set these modes after checkout with `chmod 600 private.txt && chmod 644 public.txt`; view them with `ls -l`.

Run the system-information script with `bash scripts/Marchenko_Danil_system.sh` or, after making it executable, `./scripts/Marchenko_Danil_system.sh`. It calls `whoami`, `hostname`, `date`, `uname`, `df`, and `free`, then checks that the student information file exists. `ps` and `ps aux` show process snapshots; `top` refreshes process statistics interactively. A process is a running program instance; PID is its process identifier. In `top`, identify PID, USER, `%CPU`, and `%MEM` for a process actually present on your machine.

## Part B - Git and GitHub

The repository has meaningful commits for the Linux project layout, student details and utilities, Python application and tests, Docker, Jenkins, and a feature branch merged into `main`. Inspect the history with:

```bash
git status
git log
git log --oneline --graph --all
git branch -av
git remote -v
```

`.gitignore` excludes `*.log`, `backup/`, and `.env` so runtime output, backup data, and local settings are not committed. Demonstrate the rules without using actual secret values:

```bash
touch ignored-demo.log
mkdir -p backup && touch backup/local-copy.txt
git status --short --ignored | grep -E 'ignored-demo.log|backup/'
rm -f ignored-demo.log backup/local-copy.txt
```

A branch is an isolated line of development. The `development` branch adds a JSON `/ready` endpoint and a test for it; its feature commit is merged into `main`. Git records project history; GitHub hosts the shared remote repository at [jardemAI/DevOps](https://github.com/jardemAI/DevOps).

## Part C - Docker

The `Dockerfile` uses `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, and `CMD`. It packages the standard-library Python application, runs it as a non-root user, exposes port `8000`, and serves student details at `/` and `/student`. `/health` returns `OK`; `/version`, `/metadata`, and `/ready` return application version, student metadata, and readiness information. Environment variables override defaults.

On a host with Docker Engine installed:

```bash
docker build -t marchenko-danil-devops .
docker images
docker run -d --name marchenko-danil-container \
  -p 8000:8000 \
  -e STUDENT_NAME=Danil \
  -e STUDENT_SURNAME=Marchenko \
  -e STUDENT_GROUP=IT2-2303 \
  -e STUDENT_ID=41587 \
  marchenko-danil-devops
docker ps
docker ps -a
docker logs marchenko-danil-container
curl http://localhost:8000/health
curl http://localhost:8000/ready
docker exec marchenko-danil-container python -c 'print("exec works")'
docker stop marchenko-danil-container
docker start marchenko-danil-container
docker rm -f marchenko-danil-container
```

An environment variable is a named runtime setting supplied to a process. It lets one image be reused with different student values or deployment settings. Do not bake passwords, access tokens, or other secrets into an image because layers and registries can retain them; inject secrets through an approved runtime secret mechanism instead. An image is a packaged template; a container is a running or stopped instance created from an image.

`docker-compose.yml` defines the application, ports, image, and environment values. Run `docker compose up --build`, inspect with `docker compose ps`, then remove it with `docker compose down`.

## Part D - Jenkins

Create a Jenkins **Pipeline** job named exactly `Marchenko_Danil_DevOps`. Configure **Pipeline script from SCM**, SCM **Git**, repository `https://github.com/jardemAI/DevOps`, branch `*/main`, and script path `Jenkinsfile`. This repository is public, so checkout does not require credentials. Configure an automatic trigger only when Jenkins is reachable by GitHub.

The declarative pipeline has `Checkout`, `Build`, `Test`, `Docker Build`, and `Docker Run` stages. It sets the student environment values, builds and tests the application, builds a Docker image, runs a container, checks the HTTP response, and prints container logs. The Jenkins agent needs Python 3 and Docker Engine access, including permission to access the Docker daemon. A failed stage normally stops later stages and marks the build failed; fix the cause before rerunning.

The Jenkinsfile is configuration, not proof of a successful run. Docker is not installed in the current sandbox and no Jenkins server URL or job access was supplied. Therefore no Jenkins job, image, container, or successful Jenkins result is claimed. Run the pipeline on an accessible Jenkins and Docker host to produce its authentic stage and console evidence.

## Part E - Integrated workflow

```text
Linux workspace -> Git commits and merge -> GitHub -> Jenkins checkout
               -> Build -> Test -> Docker image -> Docker container -> SUCCESS
```

Linux provides the shell and operating-system tools used to create and inspect the project. Git records changes; GitHub provides the source Jenkins checks out. Jenkins automates the build and tests, then asks Docker to package and start the application. A health and student-information check verifies the launched application. The image is the reusable package and the container is its runtime instance.

## Submission status

The personalized project and PDF report are published at [jardemAI/DevOps](https://github.com/jardemAI/DevOps). Five Python unit tests and the Bash system-information script passed in the sandbox. Docker execution and a genuine Jenkins run still require a suitable host. Do not claim a successful pipeline unless the actual Jenkins run confirms it.
