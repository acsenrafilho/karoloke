# Welcome to Karol-Oke

**Karol-Oke (`karoloke`)** is a simple and easy-to-use karaoke framework designed to non technical user to  build karaoke applications with minimal effort. The project's main objective is to provide a streamlined set of tools and APIs for handling karaoke features such as:

- Supporting multiple video formats as defined in [`settings.py`](../settings.py) (`VIDEO_FORMATS`).
- Managing song libraries and playlists.
- Enabling customizable user interfaces for karaoke experiences.
- Expose the playlist to simply get the music that you want

`karoloke` aims to be accessible for both beginners and experienced developers, focusing on clarity, extensibility, and rapid development. Whether you want to create a personal karaoke app or integrate karaoke features into an existing project, Karoloke offers the essential building blocks to get started quickly.


## Installation

To install Karol-Oke, use pip:

```bash
pip install karoloke
```

## Quick Start

After installation, you can run the Karol-Oke application directly from the script call:

```bash
karoloke
```


For more details, see the [Getting Started](getting_started.md) guide.

## Contributors & How to Help

Karol-Oke is an open-source project maintained by a growing community of contributors. We welcome all forms of participation, including:

- Reporting bugs and suggesting features via [GitHub Issues](https://github.com/acsensrafilho/karoloke/issues).
- Submitting pull requests for code improvements, documentation, or new features.
- Reviewing and testing changes to ensure quality and reliability.

### How to Contribute

- Please read our [Contribution Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting changes.
- Use the commit message prefixes (`ENH:`, `BUG:`, `DOC:`, `STY:`, `TEST:`, `WIP:`) as described in the project instructions.
- Run tests with `pytest` and check coverage before submitting.
- Use `poetry` for dependency management and running tasks (see [`pyproject.toml`](../pyproject.toml)).

Your feedback and contributions help make Karol-Oke better for everyone!