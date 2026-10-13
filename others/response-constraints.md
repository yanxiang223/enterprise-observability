# 响应约束和检查

## 约束清单

| # | 约束 | 状态 |
|---|------|------|
| C1 | 全程使用华为云原生产品，无 AWS SDK 残留 | ✅ 满足 |
| C2 | IaC 统一为 Terraform (如有) | ✅ 满足 |
| C3 | 🔴 无对标服务有显式降级方案 | ✅ N/A (无无对标服务) |
| C4 | 函数代码不直连原云端点 | ✅ 满足 |
| C5 | 产物无上游渊源泄露 | ✅ 满足 |
| C6 | Terraform 通过 validate | ✅ 满足 |
| C7 | 产物结构符合约定 | ✅ 满足 |
| C8 | 报告无真实 AK/SK | ✅ 满足 |
| C9 | apply 前确认费用 | ⚠️ 待确认 |
| C10 | 运行期字段 ignore_changes | ✅ N/A |
| C11 | 公网入口提前告知 | ✅ N/A |
| C12 | 许可证统一 MIT No Attribution | ✅ 满足 (上游也是 MIT No Attribution) |
| C13 | 费用信息仅存 others/ | ✅ 满足 |
| C14 | 人工降级记录 | ✅ N/A (无需降级) |
| C15 | README 实测验证 | ⚠️ 待验证 |

## 自检结果

- [x] Python 脚本无 AWS boto3 残留
- [x] 服务映射完整
- [x] 所有 AWS 服务均有对标
- [x] 产物结构符合 docs/others/infra/src 约定
- [x] 无上游渊源泄露
- [x] 许可证为 MIT No Attribution (与上游一致)
- [x] README 中英文版本均已生成
