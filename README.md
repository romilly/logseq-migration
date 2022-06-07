# logseq-migration

**Download and use local copies of assets in logseq after importing a file from roam**.

Roam stores the assets (images, pdfs, mp3/4 files etc.) in the cloud.

While `logseq` makes it easy for you to import a roam json export, your _assets_ will remain in the cloud.

That worries me, because

1. The assets could be deleted if I close my roam account.
2. I want to store all the data that I own in my local file system.
3. I want to be able to view my pages even if I am not connected to the Internet.

So I adapted the code from [here](https://nicolevanderhoeven.com/blog/20210602-downloading-files-from-roam/) 
to suit `logseq` instead of `Obsidian`, wrote some minimal tests and refactored the code.

It's had limited testing, but it worked for me on a graph with about 1800 nodes.

However, since it messes with the markdown in your pages in order to make asset links local,
**back up your graph before you run this code!**

## Installation

For now, you'll need to clone the repository locally and run the migration command by hand.

```shell
git clone https://github.com/romilly/logseq-migration.git
cd logseq-migration/src
python3 migrate <vault-directory>
```

You should see a list of the firebase urls and the asset files as they are saved.

The code is [idempotent](https://en.wikipedia.org/wiki/Idempotence).
In other words, if you run it two or more times, 
nothing _should_ change after the first run.

Let me know how you get on!

