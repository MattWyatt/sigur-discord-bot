import discord
import pylast
from components import servo


@servo.add_servo({
    "name": "lastfm",
    "description": "commands to interface with the lastfm api",
    "author": "Saviour#8988"
})
class LastFM(servo.GroupedServo):
    def setup(self):
        lastfm_schema = {
            "discord_id": "char(18)",
            "username": "text"
        }
        self.database.make_table("lastfm", lastfm_schema)

        self.key = self.config["lastfm"]["api_key"]
        self.secret = self.config["lastfm"]["api_secret"]
        self.network = pylast.LastFMNetwork(api_key=self.key, api_secret=self.secret)

    def validate_user(self, username):
        user = self.network.get_user(username)
        try:
            user.get_registered()
        except pylast.WSError:
            return False
        return True

    def check_for_user_entry(self, user_id):
        entry = self.database.retrieve_from_table("lastfm", "discord_id", user_id)
        if entry:
            return True
        return False

    def get_track_embed(self, username, track):
        lastfm_info = {
            "Song Name": track.get_title(properly_capitalized=True),
            "Artist": track.get_artist(),
            "Album": track.get_album(),
        }
        embed = discord.Embed(type="rich",
                              color=discord.Color.red(),
                              title="Song link for {}".format(username),
                              url=track.get_url())
        embed.set_thumbnail(url=track.get_cover_image())
        for key in lastfm_info:
            embed.add_field(name=key, value=lastfm_info[key])
        return embed

    @servo.add_command({
        "name": "link",
        "description": "links your lastfm username to your discord",
        "author": "Saviour#8988"
    })
    async def link(self, context):
        if self.check_for_user_entry(context.author.id):
            await self.client.send_message(context.channel,
                                           "you have already linked your lastfm account")
            return
        if len(context.argv) <= 1:
            await self.client.send_message(context.channel,
                                           "no lastfm account supplied")
            return
        self.database.insert_into_table("lastfm", context.author.id, context.args[0])
        await self.client.send_message(context.channel,
                                       "linked lastfm user `{}` to your discord identifier"
                                       .format(context.args[0]))
        return

    @servo.add_command({
        "name": "playing",
        "aliases": ["np", "p"],
        "description": "displays the song currently playing",
        "author": "Saviour#8988"
    })
    async def playing(self, context):
        entry = self.database.retrieve_from_table("lastfm", "discord_id", context.author.id)
        if not entry:
            await self.client.send_message(context.channel,
                                           "you do not have a lastfm account currently linked")
            return
        username = self.database.retrieve_from_table("lastfm", "discord_id", context.author.id)
        # first of the array, second of the tuple
        user = self.network.get_user(username[0][1])
        track = user.get_now_playing()
        if not track:
            embed = discord.Embed(type="rich",
                                  color=discord.Color.red(),
                                  title="Song link for {}".format(username[0][1]),
                                  url="https://blank.org/",
                                  description="this user is reveling in the silence. no song is playing.")
            await self.client.send_message(context.channel, embed=embed)
            return
        embed = self.get_track_embed(username[0][1], track)
        await self.client.send_message(context.channel, embed=embed)

    @servo.add_command({
        "name": "previous",
        "aliases": ["prev"],
        "description": "displays the last song scrobbled",
        "author": "Saviour#8988"
    })
    async def previous(self, context):
        if not self.check_for_user_entry(context.author.id):
            await self.client.send_message(context.channel,
                                           "you do not have a lastfm account currently linked")
            return

        username = self.database.retrieve_from_table("lastfm", "discord_id", context.author.id)
        # first of the array, second of the tuple
        user = self.network.get_user(username[0][1])
        track = user.get_recent_tracks(limit=2)[0].track
        embed = self.get_track_embed(username[0][1], track)
        await self.client.send_message(context.channel, embed=embed)
