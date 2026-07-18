# Strands Trader AgentCore Workshop

Website workshop Hugo được tổ chức theo format AWS Student Builder Club/First Cloud Journey, tham khảo
[`ihatesea69/aws-student-builder-club-workshop-template`](https://github.com/ihatesea69/aws-student-builder-club-workshop-template).

## Chạy local

```powershell
git submodule update --init --recursive
cd workshop
hugo server -D
```

Mở `http://localhost:1313`.

## Build

```powershell
hugo --gc --minify
```

GitHub Actions tại `.github/workflows/deploy-workshop.yml` build thư mục này và deploy lên GitHub Pages.

Kiến trúc editable nằm tại `architecture/strands-trader-agentcore.drawio`; bản SVG/PNG được đồng bộ vào
`workshop/static/images/` để hiển thị trên website.
