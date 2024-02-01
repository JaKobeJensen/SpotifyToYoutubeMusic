import os

from ytmusicapi import YTMusic

DEFAULT_AUTHENTICATION_NAME = "oauth.json"


def setup_oauth() -> None:
    os.system("ytmusicapi oauth")
    return


class YTMusicManager:
    def __init__(
        self, authentication_file_name: str | None = None, user_id: str | None = None
    ) -> None:
        self.user_id = os.environ["YouTubeUserID"] if user_id is None else user_id
        self.channel_id = os.environ["YouTubeChannelID"]
        oauth = DEFAULT_AUTHENTICATION_NAME
        if authentication_file_name is not None:
            oauth = authentication_file_name
        elif not os.path.exists("oauth.json"):
            setup_oauth()
        self.ytmusic = YTMusic(auth=oauth)
        return

    def create_playlist(self, new_playlist_name: str) -> str | dict:
        return self.ytmusic.create_playlist(new_playlist_name, "")

    def delete_playlist(
        self, playlist_id: str | None = None, playlist_name: str | None = None
    ) -> str | dict:
        if playlist_name is not None:
            playlist_id = self.get_playlist_id(playlist_name)
        return self.ytmusic.delete_playlist(playlist_id)

    def get_all_playlists_information(self) -> list[dict]:
        return [
            self.get_playlist_information(playlist["playlistId"])
            for playlist in self.ytmusic.get_library_playlists()
        ]

    def get_playlist_information(
        self,
        playlist_id: str | None = None,
        playlist_name: str | None = None,
        track_list_limit: int | None = None,
    ) -> dict:
        if playlist_name is not None:
            playlist_id = self.get_playlist_id(playlist_name)
        return self.ytmusic.get_playlist(playlist_id, track_list_limit)

    def get_playlist_id(self, playlist_name: str) -> str:
        for playlist in self.get_all_playlists_information():
            if playlist["title"] == playlist_name:
                return playlist["id"]

    def get_tracks_information_from_playlist(
        self,
        playlist_id: str | None = None,
        playlist_name: str | None = None,
        track_list_limit: int | None = None,
    ) -> list[dict]:
        return self.get_playlist_information(
            playlist_id, playlist_name, track_list_limit
        )["tracks"]

    def get_track_names_from_playlist(
        self,
        playlist_id: str | None = None,
        playlist_name: str | None = None,
        track_list_limit: int | None = None,
    ) -> list[str]:
        return [
            track["title"]
            for track in self.get_tracks_information_from_playlist(
                playlist_id, playlist_name, track_list_limit
            )
        ]

    def get_track_ids_from_playlist(
        self,
        playlist_id: str | None = None,
        playlist_name: str | None = None,
        track_list_limit: int | None = None,
    ) -> list[str]:
        return [
            track["videoId"]
            for track in self.get_tracks_information_from_playlist(
                playlist_id, playlist_name, track_list_limit
            )
        ]

    def add_tracks_to_playlist(
        self,
        track_ids: list[str],
        playlist_id: str | None = None,
        playlist_name: str | None = None,
    ) -> str | dict:
        if playlist_name is not None:
            playlist_id = self.get_playlist_id(playlist_name)
        return self.ytmusic.add_playlist_items(playlist_id, track_ids)

    def remove_all_tracks_from_playlist(
        self,
        playlist_id: str | None = None,
        playlist_name: str | None = None,
    ) -> str | dict:
        if playlist_name is not None:
            playlist_id = self.get_playlist_id(playlist_name)
        return self.ytmusic.remove_playlist_items(
            playlist_id, self.get_tracks_information_from_playlist(playlist_id)
        )

    def remove_tracks_from_playlist(
        self,
        tracks_information: list[dict],
        playlist_id: str | None = None,
        playlist_name: str | None = None,
    ) -> str | dict:
        if playlist_name is not None:
            playlist_id = self.get_playlist_id(playlist_name)
        return self.ytmusic.remove_playlist_items(playlist_id, tracks_information)

    def search_for_track_id(self, track_name: str, track_artist_name: str = "") -> str:
        return self.ytmusic.search(track_name + track_artist_name, "songs", limit=1)[0][
            "videoId"
        ]

    def search_for_track(self, track_name: str, track_artist_name: str = "") -> str:
        return self.ytmusic.search(track_name + track_artist_name, "songs", limit=1)[0]


if __name__ == "__main__":
    ytmusic_manager = YTMusicManager()
    ytmusic_manager.create_playlist("Test")
    track_ids = []
    track_ids.append(ytmusic_manager.search_for_track_id("20 Min", "Lil Uzi Vert"))
    track_ids.append(
        ytmusic_manager.search_for_track_id("22 (Taylor's Version)", "Taylor Swift")
    )
    track_ids.append(
        ytmusic_manager.search_for_track_id(
            "Algo Me Gusta De Ti", "Wisin & Yandel, Chris Brown, T-Pain"
        )
    )
    ytmusic_manager.add_tracks_to_playlist(track_ids, playlist_name="Test")
    tracks_information = ytmusic_manager.get_tracks_information_from_playlist(
        playlist_name="Test"
    )
    track_names = ytmusic_manager.get_track_names_from_playlist(playlist_name="Test")
    new_track_ids = ytmusic_manager.get_track_ids_from_playlist(playlist_name="Test")
    tracks_information = ytmusic_manager.get_tracks_information_from_playlist(
        playlist_name="Test"
    )
    ytmusic_manager.remove_tracks_from_playlist(
        [tracks_information[0]], playlist_name="Test"
    )
    ytmusic_manager.remove_all_tracks_from_playlist(playlist_name="Test")
    ytmusic_manager.delete_playlist(playlist_name="Test")
    quit()
