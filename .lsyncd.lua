-- Add sync config here

HOST     = "cam-gx-dev.gvl.org.au"
USER     = "ubuntu"             -- Remote user
SRC_DIR  = "/home/cameron/dev/galaxy/isee-dev/"   -- Trailing slash syncs dir contents only
DEST_DIR = "/home/ubuntu/isee/dev"
RSA_KEY  = "~/.ssh/gx-dev"
EXCLUDE  = { 'sync', '.lsyncd.lua', '.git' }


-- Shouldn't need to touch this:

settings {
    logfile = "/var/log/lsyncd/lsyncd.log",
    statusFile = "/var/log/lsyncd/lsyncd-status.log",
    statusInterval = 20
}

sync {
  default.rsyncssh,
  delay = 3,                    -- Sync delay after file change
  host = HOST,
  source = SRC_DIR,
  targetdir = DEST_DIR,
  exclude = EXCLUDE,
  rsync = {
    rsh = "/usr/bin/ssh -l " .. USER .. " -i " .. RSA_KEY
  }
}
