from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


class SpotifyManager:
    def __init__(self, scope: str | None = None) -> None:
        self.spotify = Spotify(auth_manager=SpotifyOAuth(scope=scope))
        self._user_id = self.spotify.me()["id"]
        return

    def create_new_playlist(self, new_playlist_name: str) -> None:
        self.spotify.user_playlist_create(self._user_id, new_playlist_name)
        return

    def get_playlists(self) -> dict:
        return self.spotify.user_playlists(self._user_id)["items"]

    def get_playlist(
        self,
        playlist_name: str | None = None,
        playlist_id: str | None = None,
    ) -> dict | None:
        if playlist_name is not None:
            for playlist in self.get_playlists():
                if playlist["name"] == playlist_name:
                    return playlist
        elif playlist_id is not None:
            return self.spotify.user_playlist(self._user_id, playlist_id)
        else:
            exit("playlist_name and playlist_id was not provided")

    def get_playlist_names(self) -> list[str]:
        return [playlist["name"] for playlist in self.get_playlists()]

    def get_playlist_ids(self) -> dict[str, str]:
        playlist_ids = {}
        for playlist in self.get_playlists():
            playlist_ids[playlist["name"]] = playlist["id"]
        return playlist_ids

    def get_tracks_from_all_playlists(self) -> list[dict]:
        playlists_tracks: list[dict] = []
        for playlist in self.get_playlists():
            if playlist["owner"]["id"] == self._user_id:
                playlist_tracks = {}
                playlist_tracks["name"] = playlist["name"]
                playlist_tracks["id"] = playlist["id"]
                playlist_tracks["tracks"] = self.get_tracks_from_playlist(
                    playlist_id=playlist["id"]
                )
                playlists_tracks.append(playlist_tracks)
        return playlists_tracks

    def get_tracks_from_playlist(
        self,
        playlist_name: str | None = None,
        playlist_id: str | None = None,
    ) -> list | None:
        playlist = self.get_playlist(
            playlist_name=playlist_name, playlist_id=playlist_id
        )
        playlist_tracks = []
        tracks = self.spotify.playlist(playlist["id"], fields="tracks,next,items")[
            "tracks"
        ]
        while tracks:
            for item in tracks["items"]:
                track = item["track"]
                playlist_tracks.append(track)
            if tracks["next"]:
                tracks = self.spotify.next(tracks)
            else:
                tracks = None
        return playlist_tracks


if __name__ == "__main__":
    spotify_manager = SpotifyManager("playlist-modify-public")
    playlist_names = spotify_manager.get_playlist_names()
    quit()
