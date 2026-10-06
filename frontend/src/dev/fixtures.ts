// Fixed synthetic content for the style preview only. Never used by the API or RAG.
export interface PreviewJob {
  id: string
  title: string
  company: string
  skills: string
  description: string
  requirement: string
  reasons: { title: string; body: string }[]
}

export const previewJobs: PreviewJob[] = [
  {
    id: 'preview-python',
    title: 'Python后端开发实习生',
    company: '演示企业 · 云杉',
    skills: 'Python · FastAPI · SQL',
    description:
      '云杉是一家专注于企业级数据与智能应用的演示企业，致力于用技术提升组织的工作效率。\n本岗位面向在校生，参与核心产品的后端服务开发与迭代。',
    requirement:
      '熟悉 Python 语言，具有使用 FastAPI 等 Web 框架进行后端开发的经验，了解关系型数据库（如 MySQL、PostgreSQL），能够进行基本的 SQL 开发。具备良好的工程意识和学习能力，对后端技术有持续的兴趣。',
    reasons: [
      {
        title: '技能匹配度高',
        body: '你的能力画像中包含 Python、FastAPI 和 SQL，与该岗位的核心技能要求高度一致，能够较快上手相关开发任务。',
      },
      {
        title: '实践经历相关',
        body: '你在项目经历中有后端开发和数据库使用的实践，具备一定的工程能力和问题解决经验，符合该岗位对实习生的能力预期。',
      },
    ],
  },
  {
    id: 'preview-data',
    title: '数据处理实习生',
    company: '演示企业 · 云帆',
    skills: 'Python · 数据分析 · SQL',
    description: '参与数据整理、质量检查和基础分析，用清晰可靠的数据支持团队的日常决策。',
    requirement:
      '掌握 Python 数据处理基础，能使用 SQL 查询数据；能够检查缺失值、重复数据并记录处理过程。',
    reasons: [
      {
        title: 'Python 与 SQL 是共同基础',
        body: '示例画像中已有 Python 和 SQL 学习经历，可以作为数据处理任务的起点。',
      },
      {
        title: '可以进一步积累数据实践',
        body: '从数据清洗和查询开始练习，补充分析过程与结果解释的能力。',
      },
    ],
  },
  {
    id: 'preview-test',
    title: '自动化测试实习生',
    company: '演示企业 · 星河',
    skills: 'Python · PyTest · Linux',
    description: '参与后端接口测试，编写和维护测试用例，帮助团队发现并复现功能问题。',
    requirement:
      '了解 HTTP 与接口测试，能够使用 Python 编写基础测试脚本；愿意学习 PyTest，并清晰记录问题。',
    reasons: [
      {
        title: '后端基础可以迁移到接口测试',
        body: '已有的 Python 和接口开发学习经历有助于理解被测试的服务。',
      },
      {
        title: '测试框架是下一步练习方向',
        body: '示例画像尚未覆盖 PyTest，需要通过具体练习补充测试设计经验。',
      },
    ],
  },
]
