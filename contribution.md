# Contributing to Elm's pyStudio

Thank you for showing interest in contributing to Elm's pyStudio! We appreciate all kinds of contributions, suggestions, and feedback. As first step we will love that you please [pass by our code of conduct](https://github.com/elmpystudio/eps/blob/main/codeOfConduct.md)

Participating in the Elm's pyStudio project does not mean to dedicate all your time, not even that
you need to contribute with big developments, from reviewing a small bug, to contribute to
document the project and finally to implement new features, all contributions will be very
rewarding for the contributor and for the community, open source helps people to feel
supported and useful no matter how small their contribution is, because all of them will result
in the improvement of the project.

## Guide to contribute

In addition to reading this guide, it is recommended that you read the general open source
contribution guide available at https://www.freecodecamp.org/news/the-definitive-guide-tocontributing-to-open-source-900d5f9f2282.
Also, it is important to know the Github guides, maybe you are already an experienced
contributor on the platform, but, if not you can review the guides at this link
https://docs.github.com/es

## Why to contribute?

Contributing to the growth, revision and improvement of Elm's pyStudio software is a way to
apply your experience as a developer, designer or user, even, an opportunity to learn and gain
experience in a project that is born with the intention of being useful to the entire community,
especially in terms of machine learning (ML) and facilitating the users without coding experience to use latest python ML technologies without writing a line! 

### Meet a comunitity with common interest

Elm's pyStudio has a welcoming and friendly community, as well as a support and a
commitment for you throughout the following years, this will allow you to find partners
and friends, a community that will allow you to grow in your professional and personal side,
finding partners for long conversations or for help in the development of Elm's pyStudio and
future projects. Make yourself at home in our community!

### Find teacher and be teacher

Working in a team in a community project implies the need to share how you do your work, as
well as to ask for help and understand how the other members of the community do theirs, all
of this is a symbiosis that will make you improve personally and professionally.

### Get you visible

Like any open source project Elm's pyStudio is 100% public, that means that your contributions
will be seen by thousands of people, thousands of professionals, head hunters and people in
the industry, the more you contribute the more you will make others see your great experience
and mastery of the subject. This will allow you to have contact with people who can
help you in your future projects

### Improve soft skills

Participating in the development of Elm's pyStudio will allow you to know in depth the people
of the community, their skills, their leadership skills, their ability to mediate conflicts, organize
work and manage teams.

## Ways To Contribute

If you have alreadydecided to collaborate, here are some smallsteps and ways to collaborate

### Reporting Issues

One of the best ways to collaborate in the project is to report issyes, this is not simply
reporting bugs, but also requesting the addition of new features or suggesting changes to
improve the behaviorof the project.
We would like you to use GitHub issues to communicate all these things to us so we can fix
them

### Contributing Code

In order to contribute code, it would be idealto consider the following issues:

- Let us know before you start working, we would like to know that the community is working on the tool.
- Comment as much as possible your code, it will be very useful for the whole community.
- Signing off on all your git commits by running `git commit -s`

Discussing your changes with the maintainers before implementation is one of the most important steps, as this sets you in the right direction before you begin. The best way to communicate this is through a detailed GitHub issue.



#### Let's contribrute!

- Fork the Repository, this is as simple as clicking on a GitHub button. Navigate to the repository https://github.com/elmpystudio/pyStudio , then click onthe **"Fork"** button at the top left.

- Once you've forked the project, clone it using:

```
git clone https://github.com/YOUR-USERNAME/pyStudio.git
```

##### Create a Upstream

Upstream is good to keep track from your repository to the original project repository.
You must be sure that your branch has the latest changes from the original repository. Note
that upstream points to the freeCodeCamp repository and not to your repository.

To create a link to the original repository, copy and paste the following command into your
terminal:
```
git remoteadd upstream <upstream address>
```

You can use 
```git pull upstream master
```
to confirm that there have been no changes up to this point (since we forked the repository until now)


##### Create a Branch

It is good to create a new branch every time you want to contribute, this allows us to identify that the branch is for the contribution you are about to make, it could be as small as correcting a typo or as long as implementing a new feature. Either way, it is good practice to create a branch.

Another important part of creating branches is the naming, it is nice to use a name that an outsider who knows nothing about the repository can easily understand. If you want to add a login functionality, for example, you should create a branch called "add-login-feature" or "loginfeature".

To create a branch you must type the following command in your terminal:

```
git checkout -b <branch-name>
```

This command will create a branch and point to it, if the branch name is "login-feature" then you can use the following command:
```
git checkout-b login-feature
```

##### Commit and Push Your Changes

Once you've made your changes, you can stage them using:

```
git add .
```

To sign your work, just add a line like this at the end of your commit message:

```
Signed-off-by: Alcon Verde <alcon.verde@pystudio.ai>
```

This can easily be done with the `-s' command-line option to append this automatically to your commit message.

```
git commit -s -m 'Meaningful commit message'
```

> In order to use the `-s` flag for auto signing the commits, you'll need to set your `user.name`and`user.email` git configs

Finally, you can push your changes to GitHub using:

```
git push origin <branch-name>
```

Once you do that and visit the repository, you should see a button on the GitHub UI prompting you to make a PR.

##### Pull Request Labels

This is the final step for any contribution to an open project, you will be saying "I have made some changes, would you mind adding them to the project". When you open a pull request, you will hope that the project owner or members like what they see and blend them. Otherwise, they may make changes or request that you make them before they blend with the stablebranch of the project.

To open a pull request, navigate to the main repository as you can see in the following image.
You will be able to see the last branch you uploaded 'login-feature', then you should click on
"'compare and pull request'." 

Clearly explain the changes you have made andthen create all PRs must have the appropriate labels based on the scope of the change. One of the following labels must be applied to Pull Requests:

If a pull request includes a new feature that does not affect existing feature sets then you'd add the `release/new-feature` label.

If a pull request includes improves an existing feature please you'd add the `release/improve-feature` label.

Pull requests containing bug fixes should have the `release/bug-fix` label.

Pull requests erlated to optimizing code fixes should have the `release/optimization` label.

Any change that breaks, or significantly alters, current behavior should be labeled with `release/breaking-change`.

The `release/documenting` label indicates that the change is associated with contents in the repo that are not associated with any code release. This would include updates to docs or tests in the repo which are not included in the release binaries.

If a pull request does not have one of these labels checks will fail and PR merging will be blocked. If you're unsure which label to apply you are still more than welcome to open the PR and a team member can help identify the correct label during the review process.

