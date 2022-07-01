import os
import sqlite3

import winbrew
import winbrew.util

class Manifest:
    """
    Stores a list of all files installed by a formula.  This class is used to
    determine which files to uninstall, and to check for conflicts between
    formulas.
    """

    def __init__(self, name):
        self.files = []
        self.name = name
        self.status = 'uninstalled'

    def save(self):
        """
        Write the manifest to the manifest file directory
        """
        values = [(path, self.name) for path in self.files]
        query = 'REPLACE INTO InstalledFile (path, formula) VALUES (?, ?)'
        self.db().cursor().executemany(query, values)
        query = 'REPLACE INTO Formula (name, status) VALUES (?, ?)'
        self.db().cursor().execute(query, (self.name, self.status))
        self.db().commit()

    def load(self):
        """
        Read the manifest from the manifest file directory
        """
        query = 'SELECT path FROM InstalledFile WHERE formula=?'
        results = self.db().cursor().execute(query, (self.name,))
        self.files = [result[0] for result in results]

        query = 'SELECT status FROM Formula where name=?'
        results = self.db().cursor().execute(query, (self.name,))
        try:
            self.status = next(results)[0]
        except StopIteration:
            pass

    def delete(self):
        """
        Delete the manifest
        """
        query = 'DELETE FROM InstalledFile WHERE formula=?'
        self.db().cursor().execute(query, (self.name,))
        query = 'DELETE FROM Formula WHERE name=?'
        self.db().cursor().execute(query, (self.name,))
        self.db().commit()

    @property
    def installed(self):
        """
        Returns true if the Manifest indicates the formula is installed
        """
        return self.status == 'installed'

    @classmethod
    def all(self):
        """
        List all installed packages
        """
        query = 'SELECT DISTINCT formula FROM InstalledFile'
        results = self.db().cursor().execute(query)
        return [Manifest(result[0]) for result in results]
        # FIXME: This may be inefficient

    @classmethod
    def db(self):
        if not getattr(self, '_db', None):
            winbrew.util.mkdir_p(winbrew.manifest_path)
            self._db = sqlite3.connect(os.path.join(winbrew.manifest_path, 'manifest.db'))
            self.migrate()
        return self._db

    @classmethod
    def migrate(self):
        """
        Execute database migrations
        """
        self._db.cursor().execute("""
        CREATE TABLE IF NOT EXISTS InstalledFile (
            path TEXT NOT NULL UNIQUE,
            formula TEXT NOT NULL,
            PRIMARY KEY(path, formula)
        )
        """)

        self._db.cursor().execute("""
        CREATE TABLE IF NOT EXISTS Formula (
            name TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL,
            PRIMARY KEY(name)
        )
        """)

