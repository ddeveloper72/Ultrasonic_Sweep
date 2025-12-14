# Heroku Buildpack Configuration

To enable FFmpeg on Heroku, you need to use a static FFmpeg buildpack:

```bash
# Login to Heroku
heroku login

# Clear existing buildpacks
heroku buildpacks:clear --app ultrasonic-sweep

# Add the static FFmpeg buildpack
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git --app ultrasonic-sweep

# Add the Python buildpack
heroku buildpacks:add --index 2 heroku/python --app ultrasonic-sweep

# Verify buildpacks are configured
heroku buildpacks --app ultrasonic-sweep
```

After adding buildpacks, redeploy:
```bash
git push heroku main
```

Or trigger a rebuild:
```bash
heroku builds:create --app ultrasonic-sweep
```

The FFmpeg buildpack will install a static build that doesn't require PulseAudio libraries.

