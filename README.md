# Parler-Data-Tools

This is a collection of python scripts and methods to parse/process/analyze bulk WARC file data from the Parler web scrape archive

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the various dependencies required for these scripts.

```bash
pip install hurry.filesize internetarchive bs4 warcat
```

## Usage

Most of these scripts are not meant to be used standalone. This is a collections of methods and code snippets that can be added to other scripts in most cases.

We are working very fast to get this stuff into a usable state for the public, but there is much work to be done.  It is unlikely you will be able to use these tools currently unless you have a basic understanding of the Python programming language and the WARC file format.

 We have tried to make sure the methods are broken into usable pieces that can be utilized in whatever tool you may be building.

**Standalone Scripts**

vidimg_extractor.py - Use this script to extract all video and image files from a given Parler WARC archive and store them for local access. Files are saved with the filename as the corresponding base64 encoded URIs. This allows us to connect them back to their occurances in the archive.

archive_grabber.py - This script can be used by passing it a collection name from archive.org. The script attempts to recursively download all files in the collection. Multithreaded, default 10 threads. 
```
Python3 archive_grabber.py <collection_name> <size_limit_in_GB> <concurrent_thread_limit>
```
**Code Snippets**

warc_parser.py - a collections of python methods that can be used to extract and relate different types of information from the Parler archives.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate. 

## License
Please give credit where credit is due, that's all we ask. We worked very hard to make this happen as a team.

[MIT](https://choosealicense.com/licenses/mit/)
