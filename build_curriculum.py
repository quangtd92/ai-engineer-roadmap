import sys
import re
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = Path(__file__).parent.resolve()

def parse_day_section(day_title, section_text, day_global_idx, day_week_idx):
    lines = section_text.strip().split('\n')
    title_clean = re.sub(r'^Ngày \d+\s*[—\-–]\s*', '', day_title).strip()
    data = {
        "global_day": day_global_idx,
        "week_day": day_week_idx,
        "raw_title": day_title,
        "title": title_clean,
        "specific_goal": "",
        "expected_outcome": "",
        "time_allocation": "",
        "theory_content": "",
        "reading_docs": "",
        "practice_task": "",
        "project_changes": "",
        "expected_files": "",
        "commands": "",
        "expected_result": "",
        "self_check_method": "",
        "dod": "",
        "commit_message": "",
        "self_check_questions": []
    }
    
    current_key = None
    buffer = []
    
    for line in lines:
        match = re.match(r'^- \*\*(.*?):\*\*\s*(.*)$', line)
        if match:
            if current_key and buffer:
                val = "\n".join(buffer).strip()
                _assign_key(data, current_key, val)
                buffer = []
            key_name = match.group(1).strip()
            first_val = match.group(2).strip()
            current_key = key_name
            if first_val:
                buffer.append(first_val)
        else:
            if current_key:
                buffer.append(line)
                
    if current_key and buffer:
        val = "\n".join(buffer).strip()
        _assign_key(data, current_key, val)
        
    return data

def _assign_key(data, key_name, val):
    k = key_name.lower()
    if "mục tiêu cụ thể" in k:
        data["specific_goal"] = val
    elif "kết quả cần đạt" in k:
        data["expected_outcome"] = val
    elif "phân bổ thời gian" in k:
        data["time_allocation"] = val
    elif "lý thuyết" in k:
        data["theory_content"] = val
    elif "tài liệu" in k:
        data["reading_docs"] = val
    elif "bài thực hành" in k:
        data["practice_task"] = val
    elif "thay đổi" in k:
        data["project_changes"] = val
    elif "file dự kiến" in k:
        data["expected_files"] = val
    elif "lệnh chạy" in k:
        data["commands"] = val
    elif "kết quả mong đợi" in k:
        data["expected_result"] = val
    elif "kiểm tra" in k:
        data["self_check_method"] = val
    elif "definition of done" in k:
        data["dod"] = val
    elif "commit" in k:
        data["commit_message"] = val
    elif "câu hỏi" in k:
        qs = [q.strip('- ').strip() for q in val.split('\n') if q.strip()]
        data["self_check_questions"] = qs

def parse_resources(res_md):
    weeks_resources = {}
    current_week = None
    lines = res_md.split('\n')
    for line in lines:
        m = re.search(r'## Tuần (\d+)', line)
        if m:
            current_week = int(m.group(1))
            weeks_resources[current_week] = []
            continue
        if current_week and line.strip().startswith('- '):
            link_m = re.search(r'- \[([^\]]+)\]\(([^)]+)\)(?::\s*(.*))?', line.strip())
            if link_m:
                weeks_resources[current_week].append({
                    "title": link_m.group(1).strip(),
                    "url": link_m.group(2).strip(),
                    "description": (link_m.group(3) or "").strip()
                })
    return weeks_resources

def linkify_reading_docs(text, week_resources):
    if not text:
        return text
    # Look for patterns like: Topic: "Title" trong [RESOURCES.md](./RESOURCES.md)
    # Match: (Topic:\s*)?[“"']([^"”']+)["”']\s*(?:trong\s*)?\[RESOURCES\.md\]\([^)]+\)
    for res in week_resources:
        title = res["title"]
        url = res["url"]
        # Try fuzzy match title in text
        # Clean title for matching
        clean_title = re.sub(r'^[^\-]+-\s*', '', title).strip()
        
        # Replace occurrences of [RESOURCES.md](...) preceded by topic/title
        pattern = r'(?:[A-Za-z0-9_\-]+\s*:\s*)?["“\']?' + re.escape(clean_title) + r'["”\']?\s*(?:trong\s*)?\[RESOURCES\.md\]\([^)]+\)'
        replacement = f'[{title}]({url})'
        if re.search(pattern, text, re.IGNORECASE):
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            
    # Generic replacement for any remaining [RESOURCES.md](...)
    if '[RESOURCES.md]' in text or 'RESOURCES.md' in text:
        if week_resources:
            # Replace [RESOURCES.md](./RESOURCES.md) with first relevant resource link or list of links
            res_links = ", ".join([f'[{r["title"]}]({r["url"]})' for r in week_resources[:3]])
            text = text.replace('trong [RESOURCES.md](./RESOURCES.md)', f'xem {res_links}')
            text = text.replace('[RESOURCES.md](./RESOURCES.md)', res_links)
            text = text.replace('[README tháng](./README.md#tài-liệu-tham-khảo-đã-chọn)', res_links)
            
    return text

def build_all():
    curriculum = {
        "months": []
    }
    
    month_names = [
        ("Month-01", "Tháng 01", "Python, FastAPI, Docker & PyTorch Foundation"),
        ("Month-02", "Tháng 02", "Data Processing, ML Foundation & Transformer"),
        ("Month-03", "Tháng 03", "LLM, Structured Output, Tool Calling & MCP"),
        ("Month-04", "Tháng 04", "RAG, Hybrid Retrieval, Reranking & Evaluation"),
        ("Month-05", "Tháng 05", "LangGraph Agent, Reliability & Human-in-the-Loop"),
        ("Month-06", "Tháng 06", "Production, AWS EC2, CI/CD & Observability")
    ]
    
    global_day_counter = 1
    
    for m_idx, (folder_name, m_label, m_desc) in enumerate(month_names, 1):
        m_dir = BASE_DIR / folder_name
        m_data = {
            "month_num": m_idx,
            "folder": folder_name,
            "title": m_label,
            "description": m_desc,
            "resources_markdown": "",
            "weeks": []
        }
        
        resources_by_week = {}
        res_file = m_dir / "RESOURCES.md"
        if res_file.exists():
            m_data["resources_markdown"] = res_file.read_text(encoding='utf-8')
            resources_by_week = parse_resources(m_data["resources_markdown"])
            
        for w_idx in range(1, 5):
            w_file = m_dir / f"Week-{w_idx:02d}.md"
            if not w_file.exists():
                continue
                
            w_content = w_file.read_text(encoding='utf-8')
            w_data = {
                "week_num": w_idx,
                "file_path": f"{folder_name}/Week-{w_idx:02d}.md",
                "title": "",
                "goal": "",
                "knowledge": "",
                "project_feature": "",
                "milestone": "",
                "review_checklist": [],
                "dod": "",
                "pitfalls": [],
                "official_resources": resources_by_week.get(w_idx, []),
                "days": []
            }
            
            # Extract main sections
            title_m = re.search(r'^#\s+(.+)$', w_content, re.MULTILINE)
            if title_m:
                w_data["title"] = title_m.group(1).strip()
                
            goal_m = re.search(r'## Mục tiêu tuần\s*\n\n(.*?)(?=\n##|\Z)', w_content, re.DOTALL)
            if goal_m:
                w_data["goal"] = goal_m.group(1).strip()

            know_m = re.search(r'## Kiến thức cần đạt\s*\n\n(.*?)(?=\n##|\Z)', w_content, re.DOTALL)
            if know_m:
                w_data["knowledge"] = know_m.group(1).strip()

            feat_m = re.search(r'## Tính năng project sẽ bổ sung\s*\n\n(.*?)(?=\n##|\Z)', w_content, re.DOTALL)
            if feat_m:
                w_data["project_feature"] = feat_m.group(1).strip()

            ms_m = re.search(r'## Milestone cuối tuần\s*\n\n(.*?)(?=\n##|\Z)', w_content, re.DOTALL)
            if ms_m:
                w_data["milestone"] = ms_m.group(1).strip()

            dod_m = re.search(r'## Definition of Done\s*\n\n(.*?)(?=\n##|\Z)', w_content, re.DOTALL)
            if dod_m:
                w_data["dod"] = dod_m.group(1).strip()

            pit_m = re.search(r'## Những lỗi thường gặp\s*\n\n(.*?)(?=\n##|\Z)', w_content, re.DOTALL)
            if pit_m:
                w_data["pitfalls"] = [p.strip('- ').strip() for p in pit_m.group(1).strip().split('\n') if p.strip()]

            # Parse days
            day_parts = re.split(r'### (Ngày \d+.*)', w_content)
            day_week_counter = 1
            for d_i in range(1, len(day_parts), 2):
                day_title = day_parts[d_i].strip()
                day_text = day_parts[d_i + 1]
                day_text = re.split(r'\n## ', day_text)[0]
                calculated_global_day = (m_idx - 1) * 28 + (w_idx - 1) * 7 + day_week_counter
                day_obj = parse_day_section(day_title, day_text, calculated_global_day, day_week_counter)
                day_obj["reading_docs"] = linkify_reading_docs(day_obj["reading_docs"], w_data["official_resources"])
                w_data["days"].append(day_obj)
                global_day_counter += 1
                day_week_counter += 1
                
            m_data["weeks"].append(w_data)
            
        curriculum["months"].append(m_data)
        
    out_file = BASE_DIR / "curriculum_data.json"
    with open(out_file, "w", encoding='utf-8') as f:
        json.dump(curriculum, f, ensure_ascii=False, indent=2)
    print(f"Successfully generated {out_file} with {global_day_counter - 1} days!")

if __name__ == "__main__":
    build_all()
