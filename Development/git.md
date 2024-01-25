Git usage summary
================
Zhenguo Zhang
January 25, 2024

-   [Git architecture](#git-architecture)
    -   [Important terms](#important-terms)
-   [Common operations](#common-operations)
    -   [Commits](#commits)
    -   [Repositories](#repositories)
    -   [Tags](#tags)
    -   [Branches](#branches)
    -   [Merge branch or files](#merge-branch-or-files)
    -   [Remotes](#remotes)
-   [Github](#github)
    -   [Linking issues and pull
        requests](#linking-issues-and-pull-requests)
-   [Git hooks](#git-hooks)
-   [FAQs](#faqs)

## Git architecture

There are several stages for making changes in a git repository. First,
changes occur in a working directory, and then the changes are added to
staging area (index), finally one can commit the staged changes into the
local repository. Git records the changes (or file versions) in a file
.git/index, which records the versions of each file for working
directory, staging, and repository. When one makes changes, `git add`
and `git commit`, these file versions will change accordingly.

### Important terms

-   HEAD: the latest commit in current branch. However, when one runs
    `git checkout <commit-hash>`, the HEAD will point to that commit and
    it becomes a detached HEAD state, beacause it points to a commit
    instead of a branch.

-   Staging area: the place to hold the changes that have been added to
    the index and about to commit.

## Common operations

### Commits

-   Show existing commits

``` bash
git log
# add a tree graph
git log --graph
```

-   Add files to commit

``` git
git add <path1> [<path2> ...]
```

-   Unstage files

The following command removes the files just added to the stage index
but not committed yet.

``` bash
git reset HEAD <path1> [<path2> ...]
```

-   Remove files from index

``` bash
# remove a file from both index and local working directory
git rm <file>
# remove a file from index but keeping the copy in working directory
git rm --cache <file>
```

-   Modify last commit

Sometimes, one may want to add more changes to last commit, so that the
last commit becomes a new commit. To do so, one can run the following
commands:

``` bash
# add new changes using git add.
# The following command opens a new window to edit commit message 
git commit --amend
# to skip message edit, use the following
git commit --amend --no-edit
```

-   Find changes

One can find the changes between the working directory, the index, and
the repository, using the `git diff` command.

``` bash
# find the changes between working directory and the index
git diff
# find the changes between working directory and the repository
git diff HEAD
# find the changes between the index and the repository
git diff --cached # --cached is equivalent to --staged
# find the difference between a local branch and remote branch
git diff localbranch..origin/remotebranch
```

Add option –name-only if one wants only filenames.

Similarly, one can also check the changes between two commits

``` bash
git diff <from-commit-sha> <to-commit-sha>
```

Or one can compare two branches

``` bash
git diff <from-branch> <to-branch>
#To compare a specific file, appending the file path
git diff <from-branch> <to-branch> -- </path/to/file>
# to compare with a remote branch, for example
git diff main origin/main --name-only
```

Actually, the output of `git diff` can be put into a file, which can be
used as patch to apply to the file (see `git apply` for more details).

To get the messages of the different comments between two branches, one
can use the following command:

``` bash
git log <old-branch>..<new-branch> --oneline
# for example, to get the commits missed by local branch.
git log main..origin/main --oneline
```

-   Revert changes

``` bash
# hard reset, revert changes in both index and working directory,
# so changes are invisible from current working directory and
# are not staged
git reset --hard HEAD # go back to head
git reset --hard HEAD~1 # going back one commit before HEAD
git reset --hard HEAD~2 # going back two commits before HEAD
# to undo hard reset, use the following
git reset --hard HEAD@{1} # move HEAD forward one commit 
# soft reset, compared to hard reset, it only modifies the index, but keeps
# the current version of files in working directory but staged
git reset --soft HEAD~1 # the changes made since this new HEAD are kept in working directory and staged
# similarly to undo a reset, run below
git reset --soft HEAD@{1}
# revert uncommited-changes in a file, the changes lost from working directory too.
git checkout -- <file>
```

One can find more about different operating modes of `git reset` at
[here](https://git-scm.com/docs/git-reset).

-   Show the changes in a commit

``` bash
git show <commit>
# or just a summary
git show <commit> --stat
# or show changes in a file
git show <commit> -- <filename>
```

-   Show the content of a file in a previous commit

``` bash
# print out the content of a file in a commit
git show <commit>:<filename>
# different from the following, which shows changes only
git show <commit> -- <filename>
```

-   Show the content of a file staged

``` bash
git show :<filename>
```

-   List files in a branch

``` bash
# list files in current branch
git ls-tree
# list files in a folder from another branch
git ls-tree anotherBranch:folder/name
```

-   Set uncommitted changes aside and then pop it back later

Sometimes, one makes some changes, but not complete enough to make a
commit, and also need to switch to a different branch for making
updates. In this case, one can use `git stash` to clean the working
directory by saving the uncommited changes to a stash, which can be
popped out later.

``` bash
git stash
# do something
git checkout another-branch
# checkout back
git checkout old-branch
git stash pop # re-gain the changes.
```

### Repositories

-   Clone a repo

``` git
# E.g.
git clone <git/url>
```

-   Clone a branch

``` git
git clone <git/url> --single-branch --branch <branch/name>
```

### Tags

-   Created tags

``` git
git tag <tag-name>
# or annotated tag
git tag -a <tag-name> -m <"message">
```

Note that tags are associated with specific commits, so they are
unrelated to branches: when switching branches, tags will not be
affected (visible from any branch).

-   Find changes after a tag is created

``` git
# only search annotated tags
git describe
# to search all tags
git describe --tags
```

The output has the following format: <tagname>-<num>-g<commit-id>, like
*v0.1.0-4-g17f4064*. Here <tagname> is the name of latest tag, and
<commit-id> is the current commit, <num> provides the number of commits
between the two. This output can ba a good candidate for the version of
a repo between two formal releases (i.e., tags).

-   Push tag to remote

    ``` git
    git push origin <tag-name>
    git push --follow-tags
    # or push all tags
    git push --tags
    ```

-   checkout from a tag

    ``` git
    git checkout tags/<tag> -b <new_branch>
    ```

### Branches

-   List branches

    ``` git
    # list local branches, current branch in green
    git branch
    # list all branches, including remote ones
    git branch -a
    ```

-   Switch branches

    ``` git
    git checkout <new-branch>
    # add option -b to create the branch if non-existent
    git checkout -b <new-branch>
    ```

-   Push to remote repo

    If the branch already exists in remote, use `git   git push`

    If the branch isn’t in remote repo, use
    `git push -u origin <branch-name>` And this command will push local
    content to remote and link local branch to the remote one.

-   Set upstream branch

    If one creates a local branch and wants to link it to a remote
    **existing** upstream branch, he can do this:
    `git   git branch --set-upstream-to=origin/<remote-branch>`

-   Delete a local branch

    ``` git
    git branch -d <branch-name>
    ```

    Note you can’t delete current branch, so switch to a different
    branch before deleting current one.

-   Delete a remote branch

    ``` git
    git push origin :<remote-branch>
    ```

-   Delete local cache of deleted remote branches

    ``` git
    git fetch -p
    ```

-   Pull from remote branches

    Git pull first runs `git fetch` to download remote commits and then
    runs `git merge` in current branch to create a local commit to
    combine both remote and local changes.

    To update a certain branch, one need to checkout that branch first.

    ``` git
    # pull onto current branche's head
    git pull
    # rebase local commits
    git pull --rebase
    ```

### Merge branch or files

-   Merge a file from another branch

        # go to the branch where the changes are merged into
        # 1. generate the patch by comparing two files
        git diff <cur-branch> <from-branch> -- /relative/file/path >tmp.patch
        # edit tmp.patch if necessary, and then apply the patch
        git apply --recount tmp.patch
        # if wants to apply the patch to the index only (not working directory),
        # add the option --cached.

-   Replace a file using the same-named file from another approach

    Different from merging, this approach will replace the file in
    current branch.

        git checkout another_branch <file-1-path> [<file-2-path> ...]

-   Merge branches

    To merge changes from one branch to another, one can use either
    `git merge` or `git rebase`. The comparison of the two can be found
    <a href="https://www.atlassian.com/git/tutorials/merging-vs-rebasing" target="_blank">here</a>.

    `git merge` creates a new merge commit and it doesn’t change
    existing commits, so it is a safe operation. The drawback is that
    one may need create many “merge commits” from upstream branch when
    developing a new feature branch. `git rebase` on the other hand will
    move (and rewrite) all new commits in new feature branch onto the
    tip of the base branch. Compared to `git merge`, `git rebase`
    provides a clearner project history. However, unless one follows all
    the
    <a href="https://www.atlassian.com/git/tutorials/merging-vs-rebasing#the-golden-rule-of-rebasing" target="_blank">rebase rules</a>,
    rebase can be dangerous to collaborators. Basically, don’t rebase a
    branch which are actively maintained by multiple developers, because
    this will cause confusion when others pull the rebased branches.

    Say, we have branches `feature` and `main`, and wants to merge the
    changes from `main` into `feature`. To do so, run the following
    command:

    ``` bash
    git checkout feature
    git merge main
    # alternatively, condense the above two commands into one as
    git merge feature main
    ```

    To use rebase, run the following

    ``` bash
    git checkout feature # DON'T rebase this branch if it is a public branch maintained by others too
    git rebase main
    ```

### Remotes

-   Add a remote to an existing local git folder

        git remote add origin <git-repo ssh or http url>

-   Show the remote url as well as branches

        git remote show origin

-   Change remote url

        git remote set-url origin <new-url>

## Github

### Linking issues and pull requests

One can link an issue with a pull request by using the keywords in the
pull request description or in commit messages. When one merge the
linked pull requests or the commits into the **default branch** (see
[here](https://docs.github.com/en/github/administering-a-repository/changing-the-default-branch)
for changing default branch ), the linked issues will be automatically
closed.

The keywords are:

-   close, closes, closed
-   fix, fixes, fixed
-   resolve, resolves, resolved

Syntax to refer to issues, in the same or different repositories
relative to pull requests:

| Issue type                      | Syntax                                 | Example                                                         |
|---------------------------------|----------------------------------------|-----------------------------------------------------------------|
| Issue in the same repository    | KEYWORD \#ISSUE-NUMBER                 | Closes \#10                                                     |
| Issue in a different repository | KEYWORD OWNER/REPOSITORY\#ISSUE-NUMBER | Fixes octo-org/octo-repo\#100                                   |
| Multiple issues                 | Use full syntax for each issue         | Resolves \#10, resolves \#123, resolves octo-org/octo-repo\#100 |

## Git hooks

To add pre-commit hooks (isort, black, and flake8), one need the
following steps: (1) install pre-commit package and add ‘pre-commit’ to
“requirements.txt”, for python project only, (2) create
.pre-commit-config.yaml (put at the root of git repo) and add hooks into
it; this file defines repos where hooks can be downloaded and high-level
options (see <https://pre-commit.com/#plugins> for more details on
option specifications), (3) run ‘pre-commit install’ to install git
hooks to .git folder. (4) if this is setup for existing repo, one can
run ‘pre-commit run –all-files’ to format existing all files. Now it is
all set, and when every time ‘git commit’ is run, the hooks would be
triggered, black formats code, and flake8 checks it, if anything
changes, the commit will fail and for you to review the changes by
black, and then you can modify code and re-commit, until no more errors.
Normally, these hooks will not prevent creating a commit, but to enforce
it, one can run ‘git config –bool flake8.strict true’ to set the
variable ‘flake8.strict’ to true, and in this way, flake8 needs be
strictly followed. Also, one can create their own hooks by following
instructions at <https://pre-commit.com/#new-hooks>.

To have all git repos install pre-commit hooks automatically, one can
run the following command:

``` bash
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir ~/.git-template
#pre-commit installed at ~/.git-template/hooks/pre-commit
```

And from now on, every time clone or init a repo, the pre-commit hook is
installed there automatically. Otherwise, one need run “pre-commit
install” to install hooks manually.

For R language, its hooks can be installed using the ‘precommit’ R
package. Simply, after installing the R package, run
‘precommit::use\_precommit()’ in fresh R session in a git repo (created
or cloned), then done. This command will create a config file
‘.precommit-hooks.yaml’ which contains R-related hooks. If the repo
already has a config file, then this command will not create a new
‘‘.precommit-hooks.yaml”, in this case, one need manually edit the file
to add hooks; refer to the config file “pre-commit-config-proj.yaml”
coming with the R package ‘precommit’ for format, which can be located
with system.file(“pre-commit-config-proj.yaml”, package=“precommit”).

## FAQs

-   Difference between HEAD, working tree, and index

    These represent different components in git architecture,
    corresponding to the different stages of files:

    -   working tree, also called working directory, is the folder
        holding all files one can view and edit.

    -   HEAD, this is a pointer which will be the parent of next commit
        or the commit to extract when checking out.

    -   index, it holds the information of all the files in current
        branch (SHA1, timestamps, and filenames), including those have
        been staged but not committed yet. So it basically holds all the
        files to be committed.
