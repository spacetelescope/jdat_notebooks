Hello @%s,

Thank you for submitting these changes to your notebook. Please read on for your technical review instructions.

## Before you begin

The technical review helps ensure that contributed notebooks a) run from top to bottom, b) follow the [PEP8 standards](https://www.python.org/dev/peps/pep-0008/) for Python code readability, and c) conform to the Institute's [style guide](https://github.com/spacetelescope/style-guides/blob/master/guides/jupyter-notebooks.md) for Jupyter Notebooks.

I've pushed the review as a new commit in this pull request. **To view and edit the commit locally, follow these steps:**

```
git checkout %s
git fetch YOUR-REMOTE-FORK
git merge YOUR-REMOTE-FORK/%s
```

_(`YOUR-REMOTE-FORK` is your fork's online copy. It's often `origin`, but if  you don't know your name for it, run `git remote -v` and choose the one whose path ends with `%s/%s.git`.)_

From here you can work on your branch as normal. If you have trouble with this step, please let me know before continuing.

---

## Instructions

After updating your local copy of this branch, **please open your notebook and address any warnings or errors you find**.

If you see cells with output like this, it means some of your code doesn't follow the PEP8 standards of code readability:

<img width="574" alt="image" src="https://user-images.githubusercontent.com/12895749/121729210-306c5300-cabc-11eb-90eb-eb494dca53c4.png">

_(In the example above, `INFO - 3:3: E111` means that the text entered on line 3 at index 3 caused the warning "E111". The violation is briefly described at the end of the message.)_

You can test that your edits satisfy the standard by installing `flake8` on the command line with:
```
pip install flake8==3.9.2 pycodestyle_magic
```

Then, restart the notebook and run the following cells:

<img width="580" alt="image" src="https://user-images.githubusercontent.com/12895749/121743209-fd7f8a80-cace-11eb-86a5-90e7b857a8be.png">

After that, edit and re-run cells with warnings until you've fixed all of them. **Please remember to delete the cells shown in the above image before pushing your changes back to this pull request.**

**If you have questions or feedback on specific cells, click the earlier message in this thread from the "review-notebook-app" bot.** There, you can comment on specific cells and view what's changed in the new commit. I may also write comments there. Anything posted there will also be reflected in this pull request's conversational thread.
