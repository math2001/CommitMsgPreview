# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
import re
import os
import json

phantom_sets = {
    # id: phantom_sets
}

EMOJI_ALIASES = re.compile(r':[a-zA-Z_]+?:')

class CommitMsgPreview(sublime_plugin.EventListener):

    def on_modified(self, view):
        if 'text.git-commit-message' not in view.scope_name(0):
            return

        first_line = view.line(0)
        text = view.substr(first_line)

        html = text.replace(' ', '&nbsp;')
        with open(os.path.join(__file__, '..', 'emojis.json')) as fp:
            for alias, base64 in json.load(fp).items():
                html = html.replace(':{}:'.format(alias),
                                    '<img src="data:image/png;base64,{0}" height="{1}" width="{1}"/>'.format(base64, view.line_height() - 2))

        length = len(EMOJI_ALIASES.sub(' ', text))
        color = 'var(--' + ('greenish' if length <= 50 else 'redish')
        html += ' <span style="color: {}"> → {}</span>'.format(color, length)

        view_id = view.id()

        ps = phantom_sets.get(view_id) or sublime.PhantomSet(view, 'commit-msg-preview')
        phantom_sets[view_id] = ps
        ps.update([
            sublime.Phantom(first_line, html, sublime.LAYOUT_BLOCK)
        ])
