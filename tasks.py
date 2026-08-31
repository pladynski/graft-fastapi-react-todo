"""
Invoke tasks for the Graftcode todo app.
Run with: inv <task-name>
"""

from invoke import task


@task
def docker_up(ctx):
    """Start Gateway + frontend with Docker Compose"""
    ctx.run("docker compose up --build")


@task
def docker_down(ctx):
    """Stop Docker Compose services"""
    ctx.run("docker compose down")


@task
def test_api(ctx):
    """Run backend TodoController unit tests"""
    with ctx.cd("backend"):
        ctx.run("python3 -m pytest test_todo_controller.py -v", env={"APP_ENV": "test"})


@task
def test_e2e(ctx):
    """Run end-to-end tests (compose stack must already be up)"""
    with ctx.cd("e2e"):
        ctx.run("python3 -m pytest test_todo_e2e.py -v")


@task
def test_all(ctx):
    """Run backend unit tests"""
    test_api(ctx)


@task
def install_frontend(ctx):
    """Install frontend dependencies and the current Gateway graft"""
    with ctx.cd("frontend"):
        ctx.run("npm install")
        ctx.run("npm run install:graft")


@task
def smoke(ctx):
    """Create/list/toggle/delete via the installed graft"""
    with ctx.cd("frontend"):
        ctx.run("npm run smoke")
