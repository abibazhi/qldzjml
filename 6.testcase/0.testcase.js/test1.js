// check-sutra-index.js

const axios = require('axios');
const cheerio = require('cheerio');

// ======================
// 1. 定义校验用例
// ======================

const testCases = [
  {
    sutraNumber: 5,
    desc: "道行般若波罗蜜经 | 晋襄阳释道安撰",
    expectedTitle: "道行般若波罗蜜经",
    expectedAuthor: "后汉月支三藏支娄迦谶译",
    testTitle: "道行般若波罗蜜经 的封面译者应为 后汉月支三藏支娄迦谶译",
    type: "translator-check"
  },
  {
    sutraNumber: 30,
    desc: "佛说法镜经 | 吴三藏沙门康僧会撰",
    expectedTitle: "佛说法镜经",
    expectedAuthor: "后汉安息国优婆塞安玄共沙门严佛调译",
    testTitle: "佛说法镜经 的封面译者应为 后汉安息国优婆塞安玄共沙门严佛调译",
    type: "translator-check"
  },
  {
    sutraNumber: 85,
    desc: "大方广佛华严经普贤菩萨行愿品 | 唐罽宾国三藏般若奉诏译",
    expectedTitle: "大方广佛华严经普贤菩萨行愿品",
    expectedAuthor: "唐罽宾国三藏般若奉诏译",
    testTitle: "大方广佛华严经普贤菩萨行愿品 经名与译者应分开",
    type: "format-issue"
  },
  {
    sutraNumber: 115,
    desc: "佛说方等泥洹经 | 失译人名附东晋录",
    expectedTitle: "佛说方等泥洹经",
    expectedAuthor: "失译人名附东晋录",
    forbiddenChars: ["今"],
    testTitle: "佛说方等泥洹经 的译者信息中不得包含'今'字",
    type: "text-validation"
  }
];

// ======================
// 2. 抓取并解析网页
// ======================

async function fetchAndValidate() {
  let results = [];

  try {
    const response = await axios.get('http://daxumi.cn/index.html');
    const $ = cheerio.load(response.data);
    const rows = $('table.dataframe tr');

    console.log('✅ 成功加载网页，开始校验...\n');

    // 遍历每一行
    rows.each((i, row) => {
      const $row = $(row);
      const cells = $row.find('td');

      if (cells.length < 3) return; // 跳过标题行或空行

      const numText = $(cells[0]).text().trim();
      if (!/^\d+$/.test(numText)) return; // 必须是数字编号

      const sutraNumber = parseInt(numText, 10);
      const title = $(cells[1]).text().trim();
      const author = $(cells[2]).text().trim();

      // 查找对应的测试用例
      const testCase = testCases.find(tc => tc.sutraNumber === sutraNumber);
      if (!testCase) return;

      const result = {
        sutraNumber,
        title,
        author,
        expectedTitle: testCase.expectedTitle,
        expectedAuthor: testCase.expectedAuthor,
        status: '✅ 正确',
        message: ''
      };

      // 校验标题
      if (title !== testCase.expectedTitle) {
        result.status = '❌ 错误';
        result.message += `标题错误：应为 "${testCase.expectedTitle}"，实际为 "${title}"`;
      }

      // 校验作者
      if (author !== testCase.expectedAuthor) {
        result.status = '❌ 错误';
        result.message += `\n译者错误：应为 "${testCase.expectedAuthor}"，实际为 "${author}"`;
      }

      // 检查禁用字符（如“今”）
      if (testCase.forbiddenChars) {
        const hasForbidden = testCase.forbiddenChars.some(char => author.includes(char));
        if (hasForbidden) {
          result.status = '❌ 错误';
          result.message += `\n包含禁用字：${author}`;
        }
      }

      // 如果之前没出错，但内容完全匹配预期，标记为正确
      if (result.status === '✅ 正确') {
        result.message = '完全匹配';
      }

      results.push(result);
    });

    // ======================
    // 3. 输出结果
    // ======================

    console.table(
      results.map(r => ({
        编号: r.sutraNumber,
        标题: r.title,
        实际译者: r.author,
        应为译者: r.expectedAuthor,
        状态: r.status,
        说明: r.message
      }))
    );

    // 统计
    const errors = results.filter(r => r.status === '❌ 错误').length;
    console.log(`\n📊 总计校验 ${results.length} 条，发现 ${errors} 处错误。\n`);

    if (errors > 0) {
      console.log('🚨 建议：请修正上述错误，确保元数据准确性。');
    } else {
      console.log('🎉 所有校验通过，目录数据准确！');
    }

  } catch (error) {
    console.error('❌ 抓取网页失败：', error.message);
  }
}

// 运行
fetchAndValidate();
