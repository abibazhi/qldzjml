// generate-report.js

const fs = require('fs');
const path = require('path');
//const fetch = require('node-fetch');
//
// Node.js v20+ 原生支持 fetch，无需 require
// 可直接使用 global.fetch 或直接调用 fetch()
const fetch = global.fetch; // 显式引用，确保可用
//
const cheerio = require('cheerio');

// ======================
// 1. 测试用例定义
// ======================

const testCases = [
  // ✅ 第5条：以目录为准，接受“撰”而非“译”
  {
    sutraNumber: 5,
    expectedTitle: "道行般若波罗蜜经",
    expectedAuthor: "晋襄阳释道安撰", // ✅ 与目录一致，接受此为“标准答案”
    testTitle: "道行般若波罗蜜经 的封面译者应为 晋襄阳释道安撰（以目录为准）",
    type: "metadata-consistency",
    note: "尽管历史上为支娄迦谶译，但现代整理本目录署名为道安撰，故以此为准"
  },


  // === 第30条：佛说法镜经 ===
  {
    sutraNumber: 30,
    expectedTitle: "佛说法镜经",
    expectedAuthor: "后汉安息国优婆塞安玄共沙门严佛调译",
    testTitle: "佛说法镜经 的目录与正文署名为 后汉安息国优婆塞安玄共沙门严佛调译",
    type: "metadata-consistency",
    note: "封面与序误标为康僧会撰，但目录与正文一致为安玄与严佛调合译，以目录为准"
  },

  {
    sutraNumber: 30,
    expectedTitle: "佛说法镜经",
    expectedAuthor: "后汉安息国优婆塞安玄共沙门严佛调译",
    testTitle: "佛说法镜经 的封面译者应为 后汉安息国优婆塞安玄共沙门严佛调译",
    type: "translator-check"
  },
  {
    sutraNumber: 85,
    expectedTitle: "大方广佛华严经普贤菩萨行愿品",
    expectedAuthor: "唐罽宾国三藏般若奉诏译",
    testTitle: "大方广佛华严经普贤菩萨行愿品 经名与译者应分开",
    type: "format-issue"
  },
  {
    sutraNumber: 115,
    expectedTitle: "佛说方等泥洹经",
    expectedAuthor: "失译人名附东晋录",
    forbiddenChars: ["今"],
    testTitle: "佛说方等泥洹经 的译者信息中不得包含'今'字",
    type: "text-validation"
  },
  {
	  desc: "128. 不必定入定入印经 | 正确应为：元魏婆罗门瞿昙般若流支译",
	  testTitle: "不必定入定入印经 的译者信息应包含结尾的'译'字",
	  type: "text-completeness",
	  expectedEndsWith: "译",
	  expected: "元魏婆罗门瞿昙般若流支译",
	  shouldNotBe: "元魏婆罗门瞿昙般若流支", // 常见错误形式
	  issue: "条目中缺少结尾的'译'字，如写成'瞿昙般若流支'而非'瞿昙般若流支译'",
	  fixSuggestion: "在译者信息末尾补上'译'字",
	  actualSelector: "#sutra-128 .translator"
  },
  {
	  desc: "131. 法华三昧经 | 正确应为：宋凉州沙门释智严译",
	  testTitle: "法华三昧经 的译者信息应包含结尾的'译'字",
	  type: "text-completeness",
	  expectedEndsWith: "译",
	  expected: "宋凉州沙门释智严译",
	  shouldNotBe: "宋凉州沙门释智严",
	  issue: "条目中缺少结尾的'译'字，如写成'释智严'而非'释智严译'",
	  fixSuggestion: "在译者信息末尾补上'译'字",
	  actualSelector: "#sutra-131 .translator"
  },
  {
	  desc: "137. 缘生初胜分法本经 | 正确经名不应包含'佛说'",
	  testTitle: "缘生初胜分法本经 的经名前不应添加'佛说'二字",
	  type: "title-validation",
	  fieldName: "经名",
	  expected: "缘生初胜分法本经",
	  shouldNotStartWith: "佛说",
	  forbiddenPrefix: "佛说",
	  issue: "经名被错误地写成'佛说缘生初胜分法本经'，多加了'佛说'前缀",
	  fixSuggestion: "删除'佛说'，恢复为原始经名：缘生初胜分法本经",
	  actualSelector: "#sutra-137 .title" // 假设页面上有对应 DOM
  },
  {
	  desc: "175. 大萨遮尼乾子受记经 | 正确经名中应为'乾'，非'干'",
	  testTitle: "大萨遮尼乾子受记经 的'乾'字不应被替换为'干'",
	  type: "character-accuracy",  // 字符准确性
	  fieldName: "经名",
	  expected: "大萨遮尼乾子受记经",
	  forbiddenChar: "干",
	  requiredChar: "乾",
	  issue: "‘乾’字被误作‘干’，导致经名变为‘大萨遮尼干子受记经’，属专有名词失真",
	  fixSuggestion: "将‘干’改为‘乾’，恢复原字",
	  actualSelector: "#sutra-175 .title",
	  correctionRule: "在佛教经名中，‘尼乾子’之‘乾’不得简化为‘干’"
  },
  {
	  desc: "195. 称赞净土佛摄受经 | 封面图片缺'诏译'，但原目录完整",
	  testTitle: "称赞净土佛摄受经 的译者信息应完整保留'奉诏译'，不因封面缺漏而省略",
	  type: "source-fidelity",  // 源头保真类校验
	  fieldName: "译者",
	  expected: "唐三藏法师玄奘奉诏译",
	  sourceOfTruth: "原书内部目录",
	  discrepancy: "封面图片缺失'诏译'二字",
	  resolution: "以原书目录为准，不可因图像缺漏而删减文字",
	  issue: "数字化时可能因封面不完整而误删'诏译'，导致信息不全",
	  fixSuggestion: "即使图片不清晰，也应依据原书目录补全为'奉诏译'",
	  actualSelector: "#sutra-195 .translator"
  },
  {
	  sutraNumber: 212,
	  title: "菩萨睒子经一卷",
	  catalogInfo: "开元録云失译人名附西晋",
	  testTitle: "菩萨睒子经属于'五经同卷'特殊装帧，封面无独立经名与译者",
	  type: "special-structure",
	  structure: "multi-text-scroll", // 多经合一卷
	  coverLabel: "五经同卷",
	  hasIndividualCover: false,     // 无独立封面
	  metadataSource: "internal-colophon", // 元数据来自内文题记或目录
	  issue: "该经与其他四部短经合为一卷，封面仅标'五经同卷'，不列具体经名与译者",
	  implication: "不可因封面缺失信息而误判为数据不全；需通过合卷内目录或题记确认归属",
	  advice: "校对时应检查合卷内部目录或各经起始处题记，以确认译者与经名",
	  actualSelector: "#sutra-212 .cover-title",
	  expectedOnCover: "五经同卷",   // 封面应有内容
	  warningIf: "封面出现具体经名或译者（可能归属错误）"
  }






];

// ======================
// 2. HTML 报告模板
// ======================

function generateHtmlReport(results) {
  const passed = results.filter(r => r.status === '✅ 正确').length;
  const failed = results.length - passed;

  const rows = results.map(r => `
    <tr class="${r.status === '✅ 正确' ? 'pass' : 'fail'}">
      <td>${r.sutraNumber}</td>
      <td>${r.title}</td>
      <td>${r.author}</td>
      <td>${r.expectedAuthor}</td>
      <td>${r.status}</td>
      <td>${r.message.replace(/\n/g, '<br>')}</td>
    </tr>
  `).join('');

  return `
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8" />
  <title>佛典目录校验报告</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      font-family: "Segoe UI", sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 1200px;
      margin: 40px auto;
      padding: 20px;
      background: #f9f9fb;
    }
    h1, h2 { text-align: center; }
    .summary {
      text-align: center;
      padding: 20px;
      background: #e6f7ff;
      border-radius: 8px;
      margin-bottom: 30px;
      font-size: 1.2em;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      background: white;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    th, td {
      padding: 12px 15px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    th {
      background: #005a9c;
      color: white;
      font-weight: bold;
    }
    tr.pass:hover { background: #f0f9f0; }
    tr.fail:hover { background: #fff0f0; }
    .pass { background: #f0f9f0; }
    .fail { background: #fff0f0; }
    .fail td { color: #c00; }
    .footer {
      text-align: center;
      margin-top: 40px;
      color: #777;
      font-size: 0.9em;
    }
  </style>
</head>
<body>
  <h1>📜 佛典目录校验报告</h1>
  <div class="summary">
    共校验 ${results.length} 条，通过 ${passed} 条，失败 ${failed} 条。
  </div>

  <table>
    <thead>
      <tr>
        <th>编号</th>
        <th>标题</th>
        <th>实际译者</th>
        <th>应为译者</th>
        <th>状态</th>
        <th>说明</th>
      </tr>
    </thead>
    <tbody>
      ${rows}
    </tbody>
  </table>

  <div class="footer">
    生成时间: ${new Date().toLocaleString('zh-CN')}
  </div>
</body>
</html>
  `;
}

// ======================
// 3. 主校验逻辑
// ======================

async function runValidation() {
  const results = [];
  const failedCases = [];

  try {
    const response = await fetch('http://daxumi.cn/index.html');
    const html = await response.text();
    const $ = cheerio.load(html);

    $('table.dataframe tr').each((i, row) => {
      const $row = $(row);
      const cells = $row.find('td');

      if (cells.length < 3) return;
      const numText = $(cells[0]).text().trim();
      if (!/^\d+$/.test(numText)) return;

      const sutraNumber = parseInt(numText, 10);
      const title = $(cells[1]).text().trim();
      const author = $(cells[2]).text().trim();

      const testCase = testCases.find(tc => tc.sutraNumber === sutraNumber);
      if (!testCase) return;

      let status = '✅ 正确';
      let message = '完全匹配';

      if (title !== testCase.expectedTitle) {
        status = '❌ 错误';
        message = `标题错误：应为 "${testCase.expectedTitle}"，实际为 "${title}"`;
      }

      if (author !== testCase.expectedAuthor) {
        status = '❌ 错误';
        message += `\n译者错误：应为 "${testCase.expectedAuthor}"，实际为 "${author}"`;
      }

      if (testCase.forbiddenChars) {
        const hasForbidden = testCase.forbiddenChars.some(char => author.includes(char));
        if (hasForbidden) {
          status = '❌ 错误';
          message = `包含禁用字：${author}`;
        }
      }

      const result = { sutraNumber, title, author, expectedAuthor: testCase.expectedAuthor, status, message };
      results.push(result);

      if (status === '❌ 错误') {
        failedCases.push(result);
      }
    });

    // ======================
    // 4. 输出到控制台（仅失败项）
    // ======================

    if (failedCases.length === 0) {
      console.log('🎉 所有校验通过！');
    } else {
      console.log(`\n🚨 发现 ${failedCases.length} 个错误：`);
      failedCases.forEach(fc => {
        console.log(`  编号 ${fc.sutraNumber}: ${fc.message.split('\n')[0]}`);
      });
    }

    // ======================
    // 5. 生成 HTML 报告
    // ======================

    const reportHtml = generateHtmlReport(results);
    const reportPath = path.join(__dirname, 'report.html');
    fs.writeFileSync(reportPath, reportHtml, 'utf-8');

    console.log(`\n📄 报告已生成：${path.resolve(reportPath)}\n`);

  } catch (error) {
    console.error('❌ 抓取失败:', error.message);
  }
}

// 执行
runValidation();
