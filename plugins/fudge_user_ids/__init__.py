# Fudge committer and author ids that git fast-import considers invalid
# Copyright 2020 Codethink Ltd

import re
import sys

from mercurial import templatefilters


def build_filter(args):
    return Filter(args)


class Filter:
    # What git considers valid (see parse_ident() in fast-import.c)
    _valid_id_re = re.compile(rb'^[^<>]* <[^<>]+>$')

    # Special characters we may need to replace
    _id_special_re = re.compile(rb'[<>]')

    def __init__(self, args):
        pass

    def commit_message_filter(self, commit_data):
        for key in ['author', 'committer']:
            user_id = commit_data[key]

            if self._valid_id_re.match(user_id):
                continue

            name = templatefilters.person(user_id)
            email = templatefilters.email(user_id)

            # Replace any special characters left in the name and email
            name = self._id_special_re.sub(b'?', name)
            email = self._id_special_re.sub(b'?', email)

            commit_data[key] = b'%s <%s>' % (name, email)

            sys.stderr.write(
                'Replaced %s id "%s" with "%s"\n'
                % (key,
                   user_id.decode('utf-8', errors='replace'),
                   commit_data[key].decode('utf-8', errors='replace')))
