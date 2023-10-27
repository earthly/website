---
title: Earthly 0.3.6 Released
categories:
  - News
as_related: false
excerpt: |
    Check out the latest release of Earthly 0.3.6! This update brings new features like enhanced command access and support for in-line comments. Don't miss out on the improved autocompletion and user terminal environment variable pass-along.
last_modified_at: 2023-07-14
---
Release Notes:

- Introduced `--ssh` flag for `RUN` which allows commands to access the ssh authentication host agent via the socket `$SSH_AUTH_SOCK` (fixes [#292](https://github.com/earthly/earthly/pull/292))
- Pass along user terminal environment variable to interactive debugger (fixes [#293](https://github.com/earthly/earthly/pull/293))
- Support for in-line comments (fixes [#288](https://github.com/earthly/earthly/pull/288))
- Fix autocompletion bug when Earthfile is invalid (fixes [#299](https://github.com/earthly/earthly/pull/299))

Documentation:

[`--ssh` documentation](https://docs.earthly.dev/earthfile#ssh)

[Release Page](https://github.com/earthly/earthly/releases/tag/v0.3.6)
