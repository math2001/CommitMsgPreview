# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
import re

phantom_sets = {
    # id: phantom_sets
}

EMOJI_ALIASES = re.compile(r':.+?:')

class CommitMsgPreview(sublime_plugin.EventListener):

    def on_modified(self, view):
        if 'text.git-commit-message' not in view.scope_name(0):
            return

        first_line = view.line(0)
        text = view.substr(first_line)
        text = EMOJI_ALIASES.sub('?', text)
        length = len(text)
        color = 'var(--' + ('greenish' if length <= 50 else 'redish')
        text = text.replace(' ', '&nbsp;')
        text += ' <span style="color: {}">| {}</span>'.format(color, length)

        view_id = view.id()

        ps = phantom_sets.get(view_id) or sublime.PhantomSet(view, 'commit-msg-preview')
        phantom_sets[view_id] = ps
        ps.update([
            sublime.Phantom(first_line, text, sublime.LAYOUT_BLOCK)
        ])
