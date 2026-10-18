# DevOps Laboratory Work 1 - Danil Marchenko

**Student:** Danil Marchenko  
**Group:** IT2-2303  
**Student ID:** 41587  
**Course:** DevOps  
**GitHub:** [jardemAI/DevOps](https://github.com/jardemAI/DevOps)

## Project layout

```text
marchenko-danil-devops/
├── app/                    # my Python HTTP application
├── assets/                 # workflow diagram source and rendering
├── backup/                 # ignored runtime backup files
├── config/app.conf
├── logs/                   # local application.log is intentionally ignored
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

I organized my project in `~/devops/marchenko-danil-devops` and created the required directories: `app`, `scripts`, `config`, `logs`, and `backup`. I added my student details to `Marchenko_Danil_info.txt` and documented non-secret application settings in `config/app.conf`. I keep the runtime log `logs/application.log` out of Git and include `logs/application.log.example` as a sample.

To recreate the local log and demonstrate the required commands, I use:

```bash
cd ~/devops/marchenko-danil-devops
cp logs/application.log.example logs/application.log
pwd
ls -la
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

I used `pwd` to print the current path, `ls` to list entries, `cd` to change directories, and `mkdir` to create a directory. `touch` creates a file or updates its timestamp; `cp` copies; `mv` moves or renames; `rm` removes; `cat` prints file contents; `head` and `tail` print the first and last lines. `find` searches by path or name. `grep` selects matching lines, and `grep -c` counts them. My sample log contains 12 lines, including 2 `ERROR` records and 3 `WARNING` records.

I set `private.txt` to mode `600` (`rw-------`), so only its owner can read or write it. I set `public.txt` to mode `644` (`rw-r--r--`), so the owner can read and write and everyone else can read. `r` means read, `w` means write, and `x` means execute for a file or directory traversal for a directory. The owner is the file's user, the group is its assigned group, and others are all remaining users. Git records the executable bit, not ordinary read/write differences, so after checkout I set the modes with `chmod 600 private.txt && chmod 644 public.txt`; I inspect them with `ls -l`.

I ran my system-information script with `bash scripts/Marchenko_Danil_system.sh` and verified that it is executable with `./scripts/Marchenko_Danil_system.sh`. The script calls `whoami`, `hostname`, `date`, `uname`, `df`, and `free`, then checks that my student information file exists. I also inspected process snapshots with `ps` and `ps aux`, and used `top` to view refreshed process statistics. A process is a running program instance; PID is its process identifier. In `top`, I identify PID, USER, `%CPU`, and `%MEM` for a process running on the machine I am using.

## Part B - Git and GitHub

I created meaningful commits for the Linux project layout and utilities, my student details, the Python application and tests, Docker, and Jenkins. I created a `development` branch, added a JSON `/ready` endpoint and a test for it, and merged that feature into `main`. I inspect my history and remotes with:

```bash
git status
git log
git log --oneline --graph --all
git branch -av
git remote -v
```

I configured `.gitignore` to exclude `*.log`, `backup/`, and `.env`, so runtime output, backup data, and local settings are not committed. I verified the rules with disposable files, without using actual secret values:

```bash
touch ignored-demo.log
mkdir -p backup && touch backup/local-copy.txt
git status --short --ignored | grep -E 'ignored-demo.log|backup/'
rm -f ignored-demo.log backup/local-copy.txt
```

A branch is an isolated line of development. I used `development` to test the `/ready` feature before merging it into `main`. Git records my project history, and I published the shared repository at [jardemAI/DevOps](https://github.com/jardemAI/DevOps).

## Part C - Docker

I wrote a `Dockerfile` using `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, and `CMD`. It packages my standard-library Python application, runs it as a non-root user, exposes port `8000`, and serves my student details at `/` and `/student`. `/health` returns `OK`; `/version`, `/metadata`, and `/ready` provide the application version, student metadata, and readiness information. Environment variables override the defaults.

On a host with Docker Engine installed, I can build and run the application with:

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

An environment variable is a named runtime setting supplied to a process. It lets me reuse one image with different student values or deployment settings. I do not bake passwords, access tokens, or other secrets into an image because layers and registries can retain them; I would supply secrets through an approved runtime secret mechanism instead. An image is a packaged template; a container is a running or stopped instance created from an image.

I configured `docker-compose.yml` with the application, ports, image, and environment values. On a Docker-enabled host, I can start it with `docker compose up --build`, inspect it with `docker compose ps`, and remove it with `docker compose down`.

I completed the Dockerfile and Compose configuration and documented commands for building the image, running the container, checking its health, and cleaning up.

## Part D - Jenkins

I wrote a declarative `Jenkinsfile` with the stages `Checkout`, `Build`, `Test`, `Docker Build`, and `Docker Run`. It sets my student environment values, runs the Python tests, builds a Docker image, starts a container, checks the HTTP response, prints container logs, and removes the container after the run.

To run it, I create a Jenkins **Pipeline** job named exactly `Marchenko_Danil_DevOps`. I configure **Pipeline script from SCM**, SCM **Git**, repository `https://github.com/jardemAI/DevOps`, branch `*/main`, and script path `Jenkinsfile`. My repository is public, so checkout does not need credentials. The Jenkins agent needs Python 3 and Docker Engine access, including permission to access the Docker daemon. I configure an automatic trigger only when Jenkins is reachable by GitHub.

When the job starts, Jenkins retrieves my Jenkinsfile and source from GitHub, assigns an agent, runs the stages in order, and records the console output and result. If a stage fails, later stages normally do not execute and Jenkins marks the build failed; I fix the cause before rerunning.

I completed the Jenkins pipeline definition and documented the SCM job settings. When I run the job, Jenkins will record each stage result and provide the console log for verification.

## Part E - Integrated workflow

```text
Linux workspace -> Git commits and merge -> GitHub -> Jenkins checkout
               -> Build -> Test -> Docker image -> Docker container -> SUCCESS
```

In my workflow, I use Linux shell and operating-system tools to create and inspect project files. Git records changes and merges; GitHub hosts my repository and provides the source Jenkins checks out. Jenkins automates the build and tests, then uses Docker to package and start my application. A health and student-information check verifies the launched application. The image is the reusable package, and the container is its runtime instance.

If a pipeline stage fails, later stages normally do not execute. Jenkins records a failed build, and I need to fix the cause before running the pipeline again. This workflow connects my local project to version control, a remote repository, automated checks, and container deployment.

## Submission status

I published my personalized project and report at [jardemAI/DevOps](https://github.com/jardemAI/DevOps). I ran five Python unit tests, my Bash system-information script, and the HTTP endpoint checks successfully. I completed the Docker and Jenkins configurations and documented their execution and verification procedures.
