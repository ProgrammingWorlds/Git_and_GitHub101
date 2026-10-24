# Git & GitHub 101: From Zero to Your First Pull Request
**Programming Worlds Academy · Beyond Code. Beyond Limits.**
دورة ثنائية اللغة (English + العربية) · Windows · Git Bash · VS Code

## What is inside / ماذا يوجد

| Item | Path |
|---|---|
| Web platform (open this) | `index.html` → `index-en.html` / `index-ar.html` |
| Lessons (36 per language) | `lesson-{module}-{1,2,3}-{en,ar}.html` |
| Lab + quiz per module (12 per language) | `lesson-{module}-lab-quiz-{en,ar}.html` |
| Full textbook PDF | `Git-and-GitHub-101-EN_Full.pdf`, `Git-and-GitHub-101-AR_Full.pdf` |
| One PDF per module | `Git-and-GitHub-101-{EN,AR}_Module01..12.pdf` |
| Cheat sheet PDF | `Git-Cheat-Sheet-{EN,AR}.pdf` |
| Cheat sheet, glossary, troubleshooting, screenshot checklist, final project and rubric (HTML) | `cheatsheet-*.html`, `glossary-*.html`, `troubleshooting-*.html`, `screenshots-*.html`, `final-project-*.html` |
| Practice project starter | `starter-project/` |
| Final project starter and sample solution | `final-project/starter/`, `final-project/solution/` |
| Brand assets, fonts, patterns | `assets/` |
| Generator source code | `source/` |

## Run it locally / تشغيل محلي
Unzip and double-click `index.html`. No server, no build step, no internet needed (fonts and logos are bundled).

## Put it on the Programming Worlds platform / الرفع على المنصة
It is a static site. Upload the whole folder (keep the structure) to any static host or to the platform's file area, and link to `index.html`. All links are relative.

## Features / الميزات
Language switch (EN/AR with RTL), light/dark theme, module sidebar, search (title and text, Arabic-normalised), progress tracking, copy buttons for command blocks, light syntax colouring of `git` commands, quiz score check (pass mark 70%), responsive layout (checked at 390 px width), print-friendly CSS.

## Progress storage / حفظ التقدم
Progress is stored in the browser (`localStorage`, key `pw-git101-v1`):
```json
{ "lessons": { "3-2": 1760000000000, "3-q": 1760000000000 }, "quizzes": { "3": { "score": 80, "ts": 1760000000000 } } }
```
It is per browser and per device. To sync with your platform accounts, replace `Store.load()` and `Store.save()` in `assets/platform.js` with calls to your API using the same JSON shape (the platform needs an authenticated endpoint such as `GET/PUT /api/progress/git-101`).

## Quizzes
Each module has a 5-question quiz and every lesson a short knowledge check. Answer order is shuffled in the HTML. Feedback appears per question; “Check my score” on the lab page records the result.

## Rebuilding / إعادة البناء
`source/` contains the Python generators (Python 3, Playwright + Chromium, pypdf). Text for lessons lives in `build*.py`; appendices in `appendix_data.py`. Run order: `build.py`, `build_m1.py` … `build_m12.py`, `platform_build.py`, `book.py`.

## Known limitations / ما يجب أن تعرفه
1. **Figures are illustrations, not real screenshots.** Each is labelled “Illustration (not a real screenshot)”. `screenshots-*.html` lists the 27 captures to take; real annotated screenshots can replace them.
2. **Git output and VS Code/GitHub UI wording were written from knowledge, not recorded from a live session.** Menu names can change; verify on a clean Windows machine before publishing.
3. **Lesson structure:** each lesson has 15 titled sections (objectives, prerequisites, introduction, explanation, analogy, diagram, commands, common mistakes, exercise, expected result, knowledge check, answers, summary, vocabulary, next lesson). Command explanations, expected output, VS Code equivalents and the guided steps are folded into “Explanation”, “Commands” and the figure rather than being separate sections. Modules 6 and others cover VS Code in more depth than later modules.
4. **Full PDF page numbers restart inside each module.** The PDF has bookmarks for navigation.
5. Final project: the lesson titles differ from the original outline (12.1 plan and start, 12.2 build with branches and pull requests, 12.3 publish), and the website requirements are covered in 12.1 with a complete sample solution.
6. GitHub Pages and plan limits change; check GitHub’s current documentation.

© Programming Worlds Academy. Logos, fonts and patterns are used as supplied in the brand identity package.
