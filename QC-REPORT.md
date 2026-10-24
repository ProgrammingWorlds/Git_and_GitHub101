# QC report (automated checks run on the final build)

- HTML pages: 109 (36 lessons + 12 lab/quiz pages per language, 5 resource pages per language, 2 home pages, 1 gate).
- Relative links and assets: all resolve (the only `style.css` match is example code shown inside lesson 3.3, not a link).
- JavaScript console errors on all pages at 390 px width: none.
- Horizontal overflow at 390 px: none.
- Each lesson page has 15 titled sections (see README, limitation 3).
- PDFs: 12 module PDFs per language (15–17 pages each), full books EN 197 pages / AR 198 pages, cheat sheets 3 pages each.
- Visual spot checks done on: covers, module openers, TOC, lesson pages (EN and AR), quiz pages, cheat sheet, platform home, sidebar, search and mobile layout. Not every page was inspected.
- Not verified: Git commands executed on a real Windows machine; VS Code and GitHub UI labels; screen-reader behaviour; contrast measured with a tool.
