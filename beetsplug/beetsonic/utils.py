"""
Utilities module
"""
from beetsplug.beetsonic import bindings


def create_subsonic_response(version, status=bindings.ResponseStatus.ok,
                             **kwargs):
    response = bindings.subsonic_response(
        version=version,
        status=status,
        **kwargs
    )
    return response


def create_artist(id, name, **kwargs):
    """
    Helper method to create an Artist object.
    :param name: Name of the artist
    :return: The Artist object
    """
    return bindings.Artist(
        id=id,
        name=name,
        **kwargs
    )


def create_song(id, title, **kwargs):
    """
    Helper method to create a Child object, representing a Song.
    :param name:
    :return: A Child object
    """
    return bindings.Child(
        id=id,
        title=title,
        isDir=False,
        **kwargs
    )


def create_indexes(artists, ignored_articles_str):
    """
    Create indexes from a list of Artist objects.
    An index consists of an uppercase character, mapping to all the Artists
    whose name starts with that character.
    :param artists: List of Artist objects.
    :param ignoredArticles: List of words to ignore while building the indexes.
    :return: An Indexes object
    """
    ignored_articles = ignored_articles_str.split(' ')
    indexes = bindings.Indexes()
    # TODO implement ignoredArticles functionality
    indexes.ignoredArticles = ignored_articles_str

    def index_func(map, artist):
        """
        The reducer function to index the list
        """
        name_parts = artist.name.split(' ')
        while name_parts[0] in ignored_articles:
            name_parts.pop(0)
        first_char = name_parts[0][:1].upper()
        if first_char not in map:
            map[first_char] = []
        map[first_char].append(artist)
        return map

    char_map = reduce(
        index_func,
        artists,
        dict()
    )
    for char, artists in sorted(char_map.iteritems()):
        index = bindings.Index(name=char)
        for artist in artists:
            index.append(artist)
        indexes.append(index)

    return indexes


def create_music_folders(music_folders):
    """
    Create a Music Folders object from a list of Music Folder objects
    :param music_folders: List of Music Folder objects
    :return: Music Folders object
    """
    folders = bindings.MusicFolders()
    for music_folder in music_folders:
        folders.append(music_folder)
    return folders


def create_music_folder(id, **kwargs):
    """
    Create a Music Folder object
    :param id: Id of the Music Folder
    :param kwargs: The other keyword arguments
    :return: The Music Folder object
    """
    return bindings.MusicFolder(
        id=id,
        **kwargs
    )


def create_songs(child_objects):
    """
    Create a Songs object from a list of Child objects.
    :param child_objects: List of Child objects.
    :return: a Songs object.
    """
    songs = bindings.Songs()
    for child in child_objects:
        songs.append(child)
    return songs
