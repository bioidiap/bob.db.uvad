from pkg_resources import resource_filename
from bob.pad.base.database import FileListPadDatabase
from bob.pad.face.database import VideoPadFile
from bob.pad.face.utils import frames, number_of_frames
import numpy
from bob.extension import rc


class File(VideoPadFile):
    """The file objects of the UVAD dataset."""
    pass


class Database(FileListPadDatabase):
    """The database interface for the UVAD dataset."""

    def __init__(self, original_directory=rc['bob.db.uvad.directory'],
                 bio_file_class=None, name='uvad',
                 original_extension=None, **kwargs):
        if bio_file_class is None:
            bio_file_class = File
        filelists_directory = resource_filename(__name__, 'lists')
        super(Database, self).__init__(
            filelists_directory=filelists_directory, name=name,
            original_directory=original_directory,
            bio_file_class=bio_file_class,
            original_extension=original_extension,
            training_depends_on_protocol=True,
            models_depend_on_protocol=True,
            **kwargs)

    def frames(self, padfile):
        """Yields the frames of the padfile one by one.

        Parameters
        ----------
        padfile : :any:`File`
            The high-level pad file

        Yields
        ------
        :any:`numpy.array`
            A frame of the video. The size is (3, 720, 1024).
        """
        vfilename = padfile.make_path(
            directory=self.original_directory,
            extension=self.original_extension)
        for frame in frames(vfilename):
            # crop frames to 720 x 1024
            h, w = numpy.shape(frame)[-2:]
            dh, dw = (h - 720) // 2, (w - 1024) // 2
            if dh != 0:
                frame = frame[:, dh:-dh, :]
            if dw != 0:
                frame = frame[:, :, dw:-dw]
            assert frame.shape == self.frame_shape, frame.shape
            yield frame

    def number_of_frames(self, padfile):
        """Returns the number of frames in a video file.

        Parameters
        ----------
        padfile : :any:`File`
            The high-level pad file

        Returns
        -------
        int
            The number of frames.
        """
        vfilename = padfile.make_path(
            directory=self.original_directory,
            extension=self.original_extension)
        return number_of_frames(vfilename)

    @property
    def frame_shape(self):
        """Returns the size of each frame in this database.

        Returns
        -------
        (int, int, int)
            The (#Channels, Height, Width) which is (3, 720, 1024).
        """
        return (3, 720, 1024)
