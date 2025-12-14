# Heroku Buildpack Configuration

To enable FFmpeg on Heroku, you need to add buildpacks using the Heroku CLI:

```bash
# Login to Heroku
heroku login

# Add the Apt buildpack (for installing system packages)
heroku buildpacks:add --index 1 heroku-community/apt --app ultrasonic-sweep

# Add the Python buildpack (should be added automatically, but ensure it's there)
heroku buildpacks:add --index 2 heroku/python --app ultrasonic-sweep

# Verify buildpacks are configured
heroku buildpacks --app ultrasonic-sweep
```

The `Aptfile` in the repository will tell the Apt buildpack to install FFmpeg.

After adding buildpacks, redeploy:
```bash
git push heroku main
```

Or trigger a rebuild:
```bash
heroku builds:create --app ultrasonic-sweep
```
