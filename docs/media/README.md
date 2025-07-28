Jellyfin is an open-source media server for streaming your personal media collection.

Here’s a sample section you can use in your ‎⁠media/README.md⁠:

Jellyfin

Jellyfin is a free, open-source media server that allows you to organize, manage, and stream your personal collection of movies, TV shows, music, and photos to a wide range of devices. It’s a self-hosted alternative to Plex and Emby, with no licensing fees or proprietary restrictions.

Key Features
 • Media Streaming: Stream your content to web browsers, mobile apps, smart TVs, and streaming devices.
 • Live TV & DVR: Integrate with TV tuners and record live television.
 • User Management: Create multiple user profiles with customizable access and parental controls.
 • Metadata Management: Automatically fetches metadata, artwork, and subtitles for your media.
 • Transcoding: Supports real-time transcoding for smooth playback on various devices.
 • Plugins: Extend functionality with a wide range of community plugins.

Docker Configuration Exampleversion: "3.8"
services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    ports:
      - "8096:8096"
    volumes:
      - /data/media:/media
      - /data/config/jellyfin:/config
    restart: unless-stopped

Why I Use Jellyfin

I chose Jellyfin for my home lab because it’s fully open-source, respects user privacy, and gives me complete control over my media experience. It integrates seamlessly with my existing storage and is easy to update and maintain using Docker.

Feel free to edit or expand this section to better fit your setup!
