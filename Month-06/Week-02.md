# Tháng 6 — Tuần 2: EC2, Nginx, HTTPS và khôi phục

## Mục tiêu tuần

Diễn tập đưa release candidate của Tuần 1 lên **một** AWS EC2 bằng Docker Compose, đặt Nginx làm reverse proxy và viết đường lui trước khi mở traffic. Việc tạo EC2, DNS và certificate là manual gate: không có tài khoản/domain thì hoàn thành đầy đủ cấu hình local và runbook, không báo cáo deploy giả.

## Kiến thức cần đạt

- Security group là firewall mạng; chỉ SSH từ CIDR quản trị, còn 80/443 mới mở công khai.
- Nginx kết thúc TLS và chuyển tiếp tới API chỉ bind loopback; nó không thay rate limit, guardrail hay approval của Month-05.
- Backup chỉ đáng tin khi có restore rehearsal; rollback image khác rollback dữ liệu volume.

## Tính năng project sẽ bổ sung

`deploy/nginx/ai-assistant-platform.conf`, `deploy/compose.ec2.yml`, `deploy/systemd/ai-assistant-platform.service`, `scripts/backup_volumes.ps1`, `scripts/rollback.ps1`, `docs/deploy-ec2.md` và phần deployment/rollback trong `docs/runbook.md`.

## Kế hoạch từng ngày

### Ngày 8 — Deployment contract và EC2 security boundary

- **Mục tiêu:** Chuyển handoff Month-05 và image RC thành một deployment contract có dependency, port và ownership rõ ràng.
- **Kết quả cần đạt:** `docs/deploy-ec2.md` có sơ đồ Internet → Nginx → `127.0.0.1:8000`, bảng biến môi trường theo *tên* và ma trận inbound SSH/HTTP/HTTPS.
- **Phân bổ thời gian:** 15 phút đọc handoff, 25 phút đọc AWS, 45 phút viết contract, 20 phút threat review = 105 phút.
- **Lý thuyết:** EC2, EBS, key pair và security group; SSH `0.0.0.0/0` không là cấu hình production.
- **Tài liệu:** [AWS EC2 getting started](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html) — instance, key pair, security group và storage.
- **Bài thực hành:** Lập checklist launch thủ công, chọn CIDR quản trị thay vì chép IP/key thật; liệt kê Redis/PostgreSQL/Qdrant nào là dependency readiness.
- **Tích hợp project:** Chốt các port và volume đúng `docker-compose.prod.yml` của Tuần 1, không thêm database mới.
- **File tạo/sửa:** `docs/deploy-ec2.md`, `deploy/README.md`.
- **Lệnh chạy:** `docker compose -f docker-compose.prod.yml config`.
- **Kết quả mong đợi:** Config render và tài liệu không chứa public IP, domain hay credential thật.
- **Cách kiểm tra:** Đối chiếu từng service/volume trong sơ đồ với Compose; `rg -n "PRIVATE KEY|BEGIN|sk-" deploy docs` không có kết quả.
- **Definition of Done:** Contract nêu rõ manual gate và điều kiện dừng deploy khi probes/quality gate fail.
- **Commit message gợi ý:** `docs(deploy): define EC2 network and dependency contract`
- **Câu hỏi tự kiểm tra:** Security group khác firewall trong container thế nào? Vì sao API không publish thẳng 8000? Dependency nào cần có trong readiness?

### Ngày 9 — Chuẩn bị host tối thiểu và runtime không đặc quyền

- **Mục tiêu:** Viết provisioning checklist có thể lặp lại cho một Linux host mà không tự động chạy lệnh đặc quyền từ CI.
- **Kết quả cần đạt:** Có checklist tạo user deploy, Docker/Compose, thư mục release và quyền đọc secret local; SSH key không được đưa vào repository.
- **Phân bổ thời gian:** 20 phút đọc Docker security, 40 phút soạn checklist, 30 phút diễn tập trên VM/local Linux, 15 phút ghi giới hạn = 105 phút.
- **Lý thuyết:** Least privilege, ownership của named volume và khác biệt giữa user trong container với user chạy Docker trên host.
- **Tài liệu:** [Docker Engine security](https://docs.docker.com/engine/security/) — Docker daemon và ranh giới quyền.
- **Bài thực hành:** Soạn `deploy/bootstrap-host.md` với placeholder `<DEPLOY_USER>`; kiểm tra service chỉ bind API loopback và secret file chmod phù hợp trên Linux.
- **Tích hợp project:** Thêm unit tài liệu vận hành image non-root đã tạo ngày 4 Tuần 1; không thay Dockerfile chỉ để phù hợp host.
- **File tạo/sửa:** `deploy/bootstrap-host.md`, `deploy/systemd/ai-assistant-platform.service`.
- **Lệnh chạy:** `docker run --rm --entrypoint id ai-assistant-platform:rc`.
- **Kết quả mong đợi:** Image vẫn là non-root; checklist có bước xác nhận Docker service và disk space trước deploy.
- **Cách kiểm tra:** Peer-review: không có `sudo` vô điều kiện, password, hoặc command xóa volume; systemd chạy Compose từ đường dẫn release xác định.
- **Definition of Done:** Có bước dừng khi host chưa harden hoặc người học chưa kiểm soát SSH key.
- **Commit message gợi ý:** `docs(deploy): add least-privilege host bootstrap checklist`
- **Câu hỏi tự kiểm tra:** Docker group có rủi ro gì? Vì sao secret file không nằm cạnh source? User container có thay user host không?

### Ngày 10 — Chuyển Compose artifact và cấu hình runtime

- **Mục tiêu:** Đóng gói release để host chạy cùng image tag và env file cục bộ, không build source trên server.
- **Kết quả cần đạt:** `compose.ec2.yml` dùng image immutable/tag release, `env_file` ignored và API chỉ publish `127.0.0.1:8000:8000`.
- **Phân bổ thời gian:** 15 phút xem Compose RC, 25 phút đọc Compose, 50 phút chỉnh/test config, 15 phút ghi hướng dẫn = 105 phút.
- **Lý thuyết:** Image promotion khác build lại; named volume tồn tại độc lập với lifecycle container.
- **Tài liệu:** [Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) — healthcheck và `depends_on`.
- **Bài thực hành:** Tạo file override EC2 không bind source, khai báo named volume có tên và kiểm tra `config` không render giá trị secret.
- **Tích hợp project:** Bảo toàn healthcheck `/health`, readiness `/ready` và các service đã dùng bởi agent checkpoint/RAG.
- **File tạo/sửa:** `deploy/compose.ec2.yml`, `deploy/.env.ec2.example`, `docs/deploy-ec2.md`.
- **Lệnh chạy:** `docker compose -f deploy/compose.ec2.yml --env-file deploy/.env.ec2.example config`.
- **Kết quả mong đợi:** YAML hợp lệ, không source mount, không cổng 8000 public.
- **Cách kiểm tra:** Tìm `ports:` và xác nhận chỉ Nginx có 80/443; inspect `env_file` mẫu chỉ thấy tên biến/giá trị giả.
- **Definition of Done:** Tài liệu mô tả copy artifact qua kênh đã được tổ chức phê duyệt, không đưa private key vào command.
- **Commit message gợi ý:** `build(deploy): add EC2 Compose release configuration`
- **Câu hỏi tự kiểm tra:** Vì sao không `git pull` rồi build trên EC2? Tag nào đủ để rollback? Named volume được tạo khi nào?

### Ngày 11 — Nginx reverse proxy và HTTP smoke test

- **Mục tiêu:** Đặt proxy trước API và kiểm tra forwarding an toàn trước khi nói tới TLS.
- **Kết quả cần đạt:** Nginx proxy được `/health` và API path tới loopback, có timeout hợp lý, request ID được chuyển tiếp và không serve file source.
- **Phân bổ thời gian:** 20 phút đọc Nginx, 45 phút viết config, 25 phút local smoke test, 15 phút xem log = 105 phút.
- **Lý thuyết:** Reverse proxy, upstream timeout, header forwarding; chỉ trust `X-Forwarded-*` khi proxy là boundary đã xác định.
- **Tài liệu:** [Nginx Beginner’s Guide](https://nginx.org/en/docs/beginners_guide.html) — server block, location và reload.
- **Bài thực hành:** Tạo server block với `proxy_pass`, giới hạn method/path cần thiết, test 200 `/health` và 502 khi upstream tắt.
- **Tích hợp project:** Giữ security headers/rate limiter FastAPI để test lại sau proxy, không chuyển logic agent vào Nginx.
- **File tạo/sửa:** `deploy/nginx/ai-assistant-platform.conf`, `tests/integration/test_reverse_proxy_contract.py`, `docs/deploy-ec2.md`.
- **Lệnh chạy:** `docker compose -f deploy/compose.ec2.yml up -d; docker compose -f deploy/compose.ec2.yml ps`.
- **Kết quả mong đợi:** Nginx là service public duy nhất; upstream API nhận request ID và `/ready` không bị cache.
- **Cách kiểm tra:** `curl -i http://localhost/health`; tắt API trong môi trường diễn tập và xác nhận Nginx trả 502, không lộ stack trace.
- **Definition of Done:** Config pass `nginx -t` trong container và test nêu rõ expected 200/502.
- **Commit message gợi ý:** `feat(proxy): add Nginx reverse proxy contract`
- **Câu hỏi tự kiểm tra:** 502 nói gì về upstream? Vì sao `/ready` không nên cache? Header nào không nên trust trực tiếp từ Internet?

### Ngày 12 — DNS, HTTPS và renewal là manual gate

- **Mục tiêu:** Viết quy trình TLS có thể thực hiện sau khi DNS ownership sẵn sàng, đồng thời có chế độ local HTTP không giả certificate.
- **Kết quả cần đạt:** Runbook kiểm tra A/AAAA record, port 80/443, xin certificate và test renewal; task được đánh dấu `NOT_RUN` nếu chưa có domain.
- **Phân bổ thời gian:** 20 phút đọc Certbot, 30 phút viết preflight, 35 phút local config/renewal dry-run, 15 phút review = 100 phút.
- **Lý thuyết:** ACME challenge chứng minh domain control; certificate và private key là secret vận hành.
- **Tài liệu:** [Certbot User Guide](https://eff-certbot.readthedocs.io/en/stable/using.html) — obtain, renew và test renewal.
- **Bài thực hành:** Ghi command mẫu bằng `<YOUR_DOMAIN>` và `--dry-run`; thêm redirect HTTP→HTTPS chỉ trong nhánh đã có certificate hợp lệ.
- **Tích hợp project:** Probe public qua Nginx tiếp tục gọi `/health`; OpenAPI/docs production theo policy ngày 1, không mở vì tiện debug.
- **File tạo/sửa:** `docs/runbook.md`, `deploy/nginx/ai-assistant-platform.conf`, `docs/deploy-ec2.md`.
- **Lệnh chạy:** `docker compose -f deploy/compose.ec2.yml config`.
- **Kết quả mong đợi:** Không có domain/cert giả trong Git; runbook nêu phương án rollback TLS config nếu reload lỗi.
- **Cách kiểm tra:** Đọc từ đầu tới cuối như operator mới: mọi command có prerequisite/expected result; chỉ chạy `certbot renew --dry-run` khi quyền/domain có thật.
- **Definition of Done:** Renewal ownership và thời điểm kiểm tra được ghi rõ; không bypass certificate warning trong tài liệu demo.
- **Commit message gợi ý:** `docs(tls): add domain-gated HTTPS and renewal procedure`
- **Câu hỏi tự kiểm tra:** DNS phải đúng trước bước nào? `--dry-run` kiểm tra gì? Vì sao không commit key TLS?

### Ngày 13 — Backup, restore rehearsal và rollback image

- **Mục tiêu:** Tách backup data khỏi rollback application và diễn tập trên fixture vô hại.
- **Kết quả cần đạt:** Có manifest volume, script tạo archive có timestamp/checksum và procedure restore vào môi trường rehearsal; rollback chọn image tag trước đó.
- **Phân bổ thời gian:** 15 phút inventory volume, 25 phút đọc backup notes, 50 phút script/rehearsal, 20 phút ghi evidence = 110 phút.
- **Lý thuyết:** RPO/RTO ở mức đơn host, consistency và lý do không copy live database file tùy tiện.
- **Tài liệu:** [Docker volumes](https://docs.docker.com/engine/storage/volumes/) — lifecycle và backup/migration volume.
- **Bài thực hành:** Backup volume fixture vào thư mục ignored/local, khôi phục vào volume rehearsal khác, chạy `/ready` và test truy vấn không nhạy cảm.
- **Tích hợp project:** Liệt kê riêng PostgreSQL/checkpoint, Qdrant và Redis persistence theo cấu hình thật; không backup `.env` vào archive.
- **File tạo/sửa:** `scripts/backup_volumes.ps1`, `scripts/rollback.ps1`, `docs/runbook.md`, `docs/backup-restore-evidence.md`.
- **Lệnh chạy:** `pwsh -File scripts/backup_volumes.ps1 -Mode rehearsal`.
- **Kết quả mong đợi:** Script dừng nếu target không phải mode rehearsal; evidence ghi archive/checksum giả định, không có dữ liệu người dùng.
- **Cách kiểm tra:** Thực hiện restore fixture rồi `docker compose ... ps`; xác nhận rollback script chỉ đổi tag/restart, không xóa volume.
- **Definition of Done:** Có test/guard cho mode rehearsal và runbook phân biệt rollback image với restore data.
- **Commit message gợi ý:** `chore(operations): add backup rehearsal and image rollback scripts`
- **Câu hỏi tự kiểm tra:** Rollback image có hoàn tác schema không? RPO là gì? Vì sao restore phải được thử?

### Ngày 14 — Milestone: deployment rehearsal và review/buffer

- **Mục tiêu:** Chạy một rehearsal có kiểm soát, đóng issue và tạo handoff CI cho Tuần 3.
- **Kết quả cần đạt:** Release candidate chạy qua Nginx local/EC2 nếu có quyền; checklist ghi probe, proxy, backup/restore và trạng thái TLS rõ ràng.
- **Phân bổ thời gian:** 15 phút chuẩn bị, 45 phút rehearsal, 20 phút smoke tests, 20 phút review/handoff = 100 phút.
- **Lý thuyết:** Deployment có thể lặp lại quan trọng hơn click-through một lần; evidence phải phân biệt PASS với NOT_RUN.
- **Tài liệu:** Xem lại `docs/deploy-ec2.md` và [Docker Compose production guidance](https://docs.docker.com/compose/how-tos/production/).
- **Bài thực hành:** Chạy config validation, image tag promotion, probes qua Nginx và rollback rehearsal; ghi blocker AWS/domain nếu không có quyền.
- **Tích hợp project:** Tạo `docs/month-06-week-02-handoff.md` liệt kê CI commands, artifact cần deploy và release criteria.
- **File tạo/sửa:** `docs/month-06-week-02-handoff.md`, `docs/runbook.md`, `docs/backup-restore-evidence.md`.
- **Lệnh chạy:** `docker compose -f deploy/compose.ec2.yml config; uv run pytest tests/integration/test_probes.py tests/integration/test_reverse_proxy_contract.py`.
- **Kết quả mong đợi:** Mọi check local pass hoặc blocker bên ngoài được ghi có owner/next action; không tạo cloud resource chỉ để đánh dấu hoàn thành.
- **Cách kiểm tra:** Review checklist bên dưới và đọc handoff để Week 3 không cần suy đoán command hay image tag.
- **Definition of Done:** Một người khác có thể diễn tập local từ runbook mà không cần secret thật.
- **Commit message gợi ý:** `docs(deploy): record EC2 rehearsal and CI handoff`
- **Câu hỏi tự kiểm tra:** Evidence nào chứng minh proxy hoạt động? Khi nào rollback thay vì sửa nóng? Điều gì khiến TLS là NOT_RUN hợp lệ?

## Milestone cuối tuần

Release candidate có deployment contract, Compose EC2, Nginx smoke test, runbook TLS theo domain gate và rehearsal backup/rollback. TLS/public EC2 chỉ được ghi `PASS` khi thực tế đã có quyền chạy.

## Review checklist

- [ ] Không có 8000 public, secret, key hoặc domain giả trong repository.
- [ ] Nginx/proxy smoke test và rollback image có expected result rõ.
- [ ] Backup restore được diễn tập trên fixture; volume không bị xóa bởi script.
- [ ] TLS là manual gate có preflight/renewal và trạng thái trung thực.

## Definition of Done

Hoàn thành bảy ngày với một deployment rehearsal kiểm chứng được; image, persistence và traffic boundary có runbook trước khi CI tự động hóa release.

## Lỗi thường gặp

- Mở SSH cho toàn Internet hoặc publish API trực tiếp.
- Gọi backup là xong mà chưa từng restore.
- Gắn volume/source bất kỳ vào Nginx hoặc container runtime.
- Coi HTTPS là hoàn tất khi DNS/challenge chưa chạy.

## Tài liệu tham khảo chính thức

Xem [RESOURCES.md](./RESOURCES.md), nhóm Tuần 2.

## Nội dung tùy chọn nếu còn thời gian

Tạo một dashboard check-list read-only cho rehearsal, hoặc đọc AWS Systems Manager overview. Không thêm autoscaling, load balancer hay IaC bắt buộc.
