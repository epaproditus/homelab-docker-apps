# Jellyfin Media Server

Jellyfin is a free software media system that puts you in control of managing and streaming your media. It's an open-source alternative to proprietary media solutions, allowing you to centralize your movie, TV show, music, and photo collections and access them from various devices.

## Purpose & Key Features

* **Personal Media Library:** Organize and stream your entire media collection.
* **No DRM:** Full control over your media; no vendor lock-in.
* **Live TV & DVR:** Record and stream live television (requires a tuner).
* **Client Support:** Access your media from web browsers, mobile apps, smart TVs, and streaming devices.
* **Transcoding:** On-the-fly media conversion to support various devices and network conditions.
* **User Management:** Create multiple users with customized access and parental controls.

## Technologies Used (Docker Compose)

Jellyfin is deployed as a Docker container, managed via Docker Compose for easy setup and persistent configuration.

### `docker-compose.yml` Example

Here's a basic `docker-compose.yml` configuration for Jellyfin. **Remember to replace the `/path/to/your/` placeholders with your actual server paths.**

```yaml
version: '3.8'
services:
  jellyfin:
    image: jellyfin/jellyfin:latest
    container_name: jellyfin
    # Using 'host' network mode for simplicity,
    # but consider a custom bridge network for better isolation in production.
    network_mode: host
    environment:
      - PUID=1000 # Your user ID (e.g., run 'id -u yourusername')
      - PGID=1000 # Your group ID (e.g., run 'id -g yourusername')
      - TZ=America/Chicago # Set your timezone, e.g., America/New_York, Europe/London
    volumes:
      - /path/to/your/jellyfin/config:/config # Persistent configuration data
      - /path/to/your/media/library:/data/media # Your main media library (movies, TV shows, music)
      - /path/to/your/transcode/cache:/data/cache # Temporary transcode cache (optional, but recommended on fast storage)
    restart: unless-stopped
