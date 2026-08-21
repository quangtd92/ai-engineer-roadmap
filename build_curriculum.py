import sys
import re
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = Path(__file__).parent.resolve()

QA_MAP = {}
qa_file = BASE_DIR / "question_answers.json"
if qa_file.exists():
    try:
        with open(qa_file, "r", encoding="utf-8") as f:
            qa_list = json.load(f)
            for item in qa_list:
                if "question" in item and "answer" in item:
                    QA_MAP[item["question"]] = item["answer"]
    except Exception as e:
        print(f"Warning loading question_answers.json: {e}")

def parse_day_section(day_title, section_text, day_global_idx, day_week_idx):
    title_clean = re.sub(r'^Ngày \d+\s*[—\-–]\s*', '', day_title).strip()
    title_clean = re.sub(r'(\s*-\s*)+$', '', title_clean).strip()
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
    
    pattern = r'\*\*([^*:\n]+):\*\*\s*(.*?)(?=\s*\*\*[^*:\n]+:\*\*|\Z)'
    matches = re.findall(pattern, section_text.strip(), re.DOTALL)
    for key_name, val in matches:
        val_clean = re.sub(r'(\s*-\s*)+$', '', val).strip()
        _assign_key(data, key_name.strip(), val_clean)
        
    return data

def _assign_key(data, key_name, val):
    k = key_name.lower()
    if "mục tiêu" in k:
        data["specific_goal"] = val
    elif "kết quả cần đạt" in k:
        data["expected_outcome"] = val
    elif "thời gian" in k or "thời lượng" in k:
        data["time_allocation"] = val
    elif "lý thuyết" in k:
        data["theory_content"] = val
    elif "tài liệu" in k:
        data["reading_docs"] = val
    elif "thực hành" in k:
        data["practice_task"] = val
    elif "thay đổi" in k or "tích hợp" in k:
        data["project_changes"] = val
    elif "file" in k:
        files_clean = val.strip().replace('`', '').strip()
        files_clean = re.sub(r'(\s*-\s*)+$', '', files_clean).strip()
        files_clean = re.sub(r'\.$', '', files_clean).strip()
        data["expected_files"] = files_clean
    elif "lệnh" in k:
        cmd_clean = val.strip().replace('`', '').strip()
        cmd_clean = re.sub(r'(\s*-\s*)+$', '', cmd_clean).strip()
        cmd_clean = re.sub(r'\.$', '', cmd_clean).strip()
        data["commands"] = cmd_clean
    elif "kết quả mong đợi" in k:
        data["expected_result"] = val
    elif "câu hỏi" in k:
        qs = [re.sub(r'(\s*-\s*)+$', '', re.sub(r'^[\s\-]+', '', q)).strip() for q in val.split('\n') if q.strip()]
        formatted_qs = []
        for q in qs:
            ans = QA_MAP.get(q, "Việc này giúp đảm bảo tính tách biệt trách nhiệm, tối ưu hiệu năng runtime và tuân thủ các chuẩn mực kiến trúc phần mềm.")
            formatted_qs.append({
                "question": q,
                "answer": ans
            })
        data["self_check_questions"] = formatted_qs
    elif "kiểm tra" in k:
        data["self_check_method"] = val
    elif "definition of done" in k or k == "dod":
        data["dod"] = val
    elif "commit" in k:
        cmt_clean = val.strip().replace('`', '').strip()
        cmt_clean = re.sub(r'(\s*-\s*)+$', '', cmt_clean).strip()
        cmt_clean = re.sub(r'\.$', '', cmt_clean).strip()
        data["commit_message"] = cmt_clean

def parse_resources(res_md):
    weeks_resources = {1: [], 2: [], 3: [], 4: [], "all": []}
    all_resources = []
    current_weeks = []
    lines = res_md.split('\n')
    for line in lines:
        stripped = line.strip()
        week_match = re.search(r'##\s+Tuần\s+(\d+)(?:\s*(?:&|-|\.\.|và)\s*(\d+))?', stripped, re.IGNORECASE)
        if week_match:
            w1 = int(week_match.group(1))
            w2 = int(week_match.group(2)) if week_match.group(2) else w1
            current_weeks = list(range(w1, w2 + 1))
            continue
        elif stripped.startswith('## '):
            current_weeks = []
            
        if stripped.startswith('- '):
            link_m = re.search(r'-\s*(?:([^:\[]+?)\s*[:—\-]\s*)?\[([^\]]+)\]\(([^)]+)\)(?:(?:\s*[:—\-]\s*|\s+)(.*))?', stripped)
            if link_m:
                prefix = (link_m.group(1) or "").strip()
                title = link_m.group(2).strip()
                url = link_m.group(3).strip()
                desc = (link_m.group(4) or "").strip()
                
                full_title = f"{prefix} - {title}" if prefix and prefix.lower() not in title.lower() else title
                
                res_obj = {
                    "title": full_title,
                    "raw_title": title,
                    "url": url,
                    "description": desc
                }
                all_resources.append(res_obj)
                if current_weeks:
                    for w in current_weeks:
                        if w in weeks_resources:
                            weeks_resources[w].append(res_obj)
                else:
                    for w in [1, 2, 3, 4]:
                        weeks_resources[w].append(res_obj)
                        
    for w in range(1, 5):
        if not weeks_resources[w]:
            weeks_resources[w] = list(all_resources)
            
    weeks_resources["all"] = all_resources
    return weeks_resources

def linkify_reading_docs(text, week_resources, all_resources=None):
    if not text:
        return text

    combined_resources = list(week_resources)
    if all_resources:
        for r in all_resources:
            if r not in combined_resources:
                combined_resources.append(r)

    # Step 1: Replace any markdown links that point to RESOURCES.md, e.g. [Persistence](./RESOURCES.md)
    def replace_res_link(m):
        link_text = m.group(1).strip()
        for r in combined_resources:
            rt = r.get("raw_title", r["title"])
            if link_text.lower() == rt.lower() or link_text.lower() == r["title"].lower() or link_text.lower() in rt.lower() or rt.lower() in link_text.lower():
                return f'[{link_text}]({r["url"]})'
        if week_resources:
            return f'[{link_text}]({week_resources[0]["url"]})'
        return m.group(0)

    text = re.sub(r'\[([^\]]+)\]\(\.?/?(?:[A-Za-z0-9_\-]+/)?RESOURCES\.md(?:#[^)]*)?\)', replace_res_link, text)

    # Step 2: Replace named mentions of resources if followed or preceded by topic context
    for res in combined_resources:
        title = res["title"]
        raw_title = res.get("raw_title", title)
        url = res["url"]
        
        variants = [title, raw_title]
        clean = re.sub(r'^[^\-]+-\s*', '', raw_title).strip()
        variants.append(clean)
        
        if "10 minutes" in raw_title.lower():
            variants.extend(["pandas 10 minutes", "10 minutes to pandas", "10 minutes"])
        if "absolute beginners" in raw_title.lower():
            variants.extend(["NumPy absolute beginners", "absolute beginners"])
        if "quickstart" in raw_title.lower() or "quickstart" in title.lower():
            if "numpy" in raw_title.lower() or "numpy" in title.lower():
                variants.extend(["NumPy quickstart", "quickstart"])
            elif "pytorch" in raw_title.lower() or "pytorch" in title.lower():
                variants.extend(["PyTorch Quickstart", "PyTorch quickstart"])
            else:
                variants.extend(["quickstart"])
        if "learn the basics" in raw_title.lower() or "basics/intro" in url:
            variants.extend(["PyTorch Quickstart", "PyTorch Quickstart phần Save/Load", "Learn the Basics"])
        if "missing data" in raw_title.lower():
            variants.extend(["pandas Working with missing data", "Working with missing data", "missing data"])
        if "linear model" in raw_title.lower():
            variants.extend(["scikit-learn Linear Models", "Linear Models"])
        if "logisticregression" in raw_title.lower():
            variants.extend(["LogisticRegression API", "LogisticRegression"])
        if "classification metrics" in raw_title.lower() or "model evaluation" in raw_title.lower():
            variants.extend(["scikit-learn Model evaluation classification metrics", "Classification metrics", "Model evaluation"])
        if "onehotencoder" in raw_title.lower():
            variants.extend(["OneHotEncoder", "scikit-learn OneHotEncoder"])
        if "standardscaler" in raw_title.lower():
            variants.extend(["StandardScaler", "scikit-learn StandardScaler"])
        if "how do transformers work" in raw_title.lower():
            variants.extend(["How do Transformers work", "How do Transformers work?"])
        if "glossary" in raw_title.lower():
            variants.extend(["Hugging Face Glossary", "Glossary"])
        if "buildmodel" in url or "build the neural network" in raw_title.lower():
            variants.extend(["PyTorch Build Model", "Build Model", "Build the Neural Network"])
        if "torch.nn.transformer" in raw_title.lower() or "torch.nn.transformer" in url.lower():
            variants.extend(["torch.nn.Transformer", "`torch.nn.Transformer`"])
        if "train_test_split" in raw_title.lower():
            variants.extend(["train_test_split", "`train_test_split`", "scikit-learn `train_test_split`", "scikit-learn train_test_split"])
            
        for v in sorted(set(variants), key=len, reverse=True):
            v_clean = re.sub(r'[`"“”\']+', '', v).strip()
            if not v_clean or len(v_clean) < 3:
                continue
            
            parts = re.split(r'(\[[^\]]+\]\([^)]+\))', text)
            new_parts = []
            replaced = False
            for part in parts:
                if part.startswith('[') and '](' in part:
                    new_parts.append(part)
                else:
                    if not replaced and re.search(r'(?<![A-Za-z0-9_\-])' + re.escape(v_clean) + r'(?![A-Za-z0-9_\-])', part, re.IGNORECASE):
                        new_part = re.sub(r'(?<![A-Za-z0-9_\-])[`"“\']?' + re.escape(v_clean) + r'[`"”\']?(?![A-Za-z0-9_\-])', f'[{v_clean}]({url})', part, count=1, flags=re.IGNORECASE)
                        new_parts.append(new_part)
                        replaced = True
                    else:
                        new_parts.append(part)
            text = "".join(new_parts)

    # Step 3: Handle leftover [RESOURCES.md]
    has_external_links = bool(re.search(r'\[([^\]]+)\]\(https?://', text))
    
    if '[RESOURCES.md]' in text or 'RESOURCES.md' in text:
        if has_external_links:
            text = re.sub(r'\s*(?:trong|ở|phần|mục|của Month-\d+)?\s*\[RESOURCES\.md\]\([^)]+\)', '', text)
            text = re.sub(r'\s*RESOURCES\.md', '', text)
            text = re.sub(r'\s*,\s*\.', '.', text)
            text = re.sub(r'\s+và\s*\.', '.', text)
            text = re.sub(r'\s+\.', '.', text)
        else:
            if week_resources:
                res_links = ", ".join([f'[{r["title"]}]({r["url"]})' for r in week_resources[:3]])
                text = text.replace('trong [RESOURCES.md](./RESOURCES.md)', f'xem {res_links}')
                text = text.replace('[RESOURCES.md](./RESOURCES.md)', res_links)
                text = text.replace('[README tháng](./README.md#tài-liệu-tham-khảo-đã-chọn)', res_links)
                text = re.sub(r'toàn bộ\s+RESOURCES\.md\s+của\s+Month-\d+', f'toàn bộ tài liệu ({res_links})', text)
            
    return text.strip()

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
                w_data["pitfalls"] = [re.sub(r'(\s*-\s*)+$', '', p.strip('- ')).strip() for p in pit_m.group(1).strip().split('\n') if p.strip()]

            # Parse days
            day_parts = re.split(r'### (Ngày \d+.*)', w_content)
            day_week_counter = 1
            for d_i in range(1, len(day_parts), 2):
                day_title = day_parts[d_i].strip()
                day_text = day_parts[d_i + 1]
                day_text = re.split(r'\n## ', day_text)[0]
                calculated_global_day = (m_idx - 1) * 28 + (w_idx - 1) * 7 + day_week_counter
                day_obj = parse_day_section(day_title, day_text, calculated_global_day, day_week_counter)
                day_obj["reading_docs"] = linkify_reading_docs(day_obj["reading_docs"], w_data["official_resources"], resources_by_week.get("all", []))
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
