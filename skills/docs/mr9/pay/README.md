總結 執行步驟上面執行步驟，產生一份開發 claude SKILLS 文檔，需求如下
- 固定資料 @ot888_bank_filtered.md
- 輸入 ${ARGS}.md ，這个資料必須包含(银行名称,银行代码)
- 合併 @ot888_bank_filtered.md 與 ${ARGS}.md ，新的合并文件包含四个字段
    1. id - 来自ot888文件的ID（332-364），只在SGpay中存在的银行用"null"
    2. 银行名称_ot888 - 来自ot888文件的银行名称，只在SGpay中存在的银行用"null"
    3. 银行名称_SGpay - 来自SGpay文件的银行名称，只在ot888中存在的银行用"null"
    4. 银行代码 - 来自SGpay文件的银行代码
- 生成SQL , sql 模版 "INSERT INTO ${tenant}_channel_bank (channel_id, bank_id, recharge_bank_code, withdraw_bank_code, currency) VALUES (1271, '#{id}', '#{银行代码}', '#{银行代码}', 'THB') ON CONFLICT
  (channel_id, bank_id) DO NOTHING;" 使用 @merged_banks.md 填充模版, id = #{id} #{银行代码}=银行代码 