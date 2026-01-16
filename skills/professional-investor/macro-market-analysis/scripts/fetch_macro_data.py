#!/usr/bin/env python3
"""
總體經濟數據自動獲取腳本
Macro Economic Data Fetcher

功能：
1. 從 FRED API 獲取美國總體經濟指標
2. 數據清洗與格式化
3. 生成 JSON 和 CSV 格式報告
4. 計算 YoY, MoM 變化率
5. 提供數據解讀建議

使用方法：
python fetch_macro_data.py --api-key YOUR_FRED_API_KEY --output ./data

依賴套件：
pip install requests pandas python-dotenv
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests
import pandas as pd
from pathlib import Path

# ============================================================================
# 配置區
# ============================================================================

# FRED API 配置
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
FRED_SERIES_URL = "https://api.stlouisfed.org/fred/series"

# 經濟指標定義（FRED Series ID）
ECONOMIC_INDICATORS = {
    # GDP 與經濟成長
    "GDP": {
        "series_id": "GDPC1",
        "name": "Real GDP",
        "name_zh": "實質 GDP",
        "unit": "Billions of Chained 2017 Dollars",
        "frequency": "Quarterly",
        "importance": "⭐⭐⭐"
    },
    "GDP_GROWTH": {
        "series_id": "A191RL1Q225SBEA",
        "name": "Real GDP Growth Rate",
        "name_zh": "實質 GDP 成長率",
        "unit": "Percent",
        "frequency": "Quarterly",
        "importance": "⭐⭐⭐"
    },
    
    # 通膨指標
    "CPI": {
        "series_id": "CPIAUCSL",
        "name": "Consumer Price Index (All Items)",
        "name_zh": "消費者物價指數（整體）",
        "unit": "Index 1982-1984=100",
        "frequency": "Monthly",
        "importance": "⭐⭐⭐"
    },
    "CORE_CPI": {
        "series_id": "CPILFESL",
        "name": "Core CPI (Ex Food & Energy)",
        "name_zh": "核心 CPI（排除食品與能源）",
        "unit": "Index 1982-1984=100",
        "frequency": "Monthly",
        "importance": "⭐⭐⭐"
    },
    "PPI": {
        "series_id": "PPIACO",
        "name": "Producer Price Index",
        "name_zh": "生產者物價指數",
        "unit": "Index 1982=100",
        "frequency": "Monthly",
        "importance": "⭐⭐"
    },
    "PCE": {
        "series_id": "PCEPI",
        "name": "Personal Consumption Expenditures Price Index",
        "name_zh": "個人消費支出物價指數",
        "unit": "Index 2017=100",
        "frequency": "Monthly",
        "importance": "⭐⭐⭐"
    },
    "CORE_PCE": {
        "series_id": "PCEPILFE",
        "name": "Core PCE (Fed's Preferred Measure)",
        "name_zh": "核心 PCE（Fed 首選指標）",
        "unit": "Index 2017=100",
        "frequency": "Monthly",
        "importance": "⭐⭐⭐"
    },
    
    # 利率與貨幣政策
    "FED_FUNDS_RATE": {
        "series_id": "FEDFUNDS",
        "name": "Federal Funds Effective Rate",
        "name_zh": "聯邦基金利率",
        "unit": "Percent",
        "frequency": "Monthly",
        "importance": "⭐⭐⭐"
    },
    "10Y_TREASURY": {
        "series_id": "DGS10",
        "name": "10-Year Treasury Constant Maturity Rate",
        "name_zh": "10 年期公債殖利率",
        "unit": "Percent",
        "frequency": "Daily",
        "importance": "⭐⭐⭐"
    },
    "2Y_TREASURY": {
        "series_id": "DGS2",
        "name": "2-Year Treasury Constant Maturity Rate",
        "name_zh": "2 年期公債殖利率",
        "unit": "Percent",
        "frequency": "Daily",
        "importance": "⭐⭐⭐"
    },
    
    # 就業指標
    "UNEMPLOYMENT_RATE": {
        "series_id": "UNRATE",
        "name": "Unemployment Rate",
        "name_zh": "失業率",
        "unit": "Percent",
        "frequency": "Monthly",
        "importance": "⭐⭐⭐"
    },
    "NONFARM_PAYROLLS": {
        "series_id": "PAYEMS",
        "name": "Nonfarm Payrolls",
        "name_zh": "非農就業人數",
        "unit": "Thousands of Persons",
        "frequency": "Monthly",
        "importance": "⭐⭐⭐"
    },
    "INITIAL_CLAIMS": {
        "series_id": "ICSA",
        "name": "Initial Jobless Claims",
        "name_zh": "初領失業救濟金人數",
        "unit": "Thousands",
        "frequency": "Weekly",
        "importance": "⭐⭐"
    },
    "AVERAGE_HOURLY_EARNINGS": {
        "series_id": "CES0500000003",
        "name": "Average Hourly Earnings",
        "name_zh": "平均時薪",
        "unit": "Dollars per Hour",
        "frequency": "Monthly",
        "importance": "⭐⭐⭐"
    },
    "LABOR_PARTICIPATION": {
        "series_id": "CIVPART",
        "name": "Labor Force Participation Rate",
        "name_zh": "勞動參與率",
        "unit": "Percent",
        "frequency": "Monthly",
        "importance": "⭐⭐"
    },
    
    # PMI 指標
    "ISM_MANUFACTURING": {
        "series_id": "MANEMP",
        "name": "ISM Manufacturing PMI",
        "name_zh": "ISM 製造業 PMI",
        "unit": "Index",
        "frequency": "Monthly",
        "importance": "⭐⭐⭐"
    },
    
    # 消費與零售
    "RETAIL_SALES": {
        "series_id": "RSXFS",
        "name": "Retail Sales (Ex Auto)",
        "name_zh": "零售銷售（排除汽車）",
        "unit": "Millions of Dollars",
        "frequency": "Monthly",
        "importance": "⭐⭐"
    },
    "CONSUMER_CONFIDENCE": {
        "series_id": "UMCSENT",
        "name": "University of Michigan Consumer Sentiment",
        "name_zh": "密西根大學消費者信心指數",
        "unit": "Index 1966:Q1=100",
        "frequency": "Monthly",
        "importance": "⭐⭐"
    },
    
    # 住房市場
    "HOUSING_STARTS": {
        "series_id": "HOUST",
        "name": "Housing Starts",
        "name_zh": "新屋開工",
        "unit": "Thousands of Units",
        "frequency": "Monthly",
        "importance": "⭐⭐"
    },
    "BUILDING_PERMITS": {
        "series_id": "PERMIT",
        "name": "New Private Housing Units Authorized",
        "name_zh": "營建許可",
        "unit": "Thousands of Units",
        "frequency": "Monthly",
        "importance": "⭐⭐"
    },
    
    # 工業生產
    "INDUSTRIAL_PRODUCTION": {
        "series_id": "INDPRO",
        "name": "Industrial Production Index",
        "name_zh": "工業生產指數",
        "unit": "Index 2017=100",
        "frequency": "Monthly",
        "importance": "⭐⭐"
    },
    "CAPACITY_UTILIZATION": {
        "series_id": "TCU",
        "name": "Capacity Utilization",
        "name_zh": "產能利用率",
        "unit": "Percent of Capacity",
        "frequency": "Monthly",
        "importance": "⭐⭐"
    }
}


# ============================================================================
# 主要類別
# ============================================================================

class MacroDataFetcher:
    """總體經濟數據獲取器"""
    
    def __init__(self, api_key: str, lookback_years: int = 5):
        """
        初始化
        
        Args:
            api_key: FRED API Key
            lookback_years: 回溯資料年數（預設 5 年）
        """
        self.api_key = api_key
        self.lookback_years = lookback_years
        self.start_date = (datetime.now() - timedelta(days=365 * lookback_years)).strftime("%Y-%m-%d")
        self.end_date = datetime.now().strftime("%Y-%m-%d")
        self.data_cache = {}
        
    def fetch_series(self, series_id: str, start_date: Optional[str] = None, 
                     end_date: Optional[str] = None) -> pd.DataFrame:
        """
        獲取單一經濟指標數據
        
        Args:
            series_id: FRED Series ID
            start_date: 開始日期 (YYYY-MM-DD)
            end_date: 結束日期 (YYYY-MM-DD)
            
        Returns:
            DataFrame with columns: date, value
        """
        start_date = start_date or self.start_date
        end_date = end_date or self.end_date
        
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "observation_start": start_date,
            "observation_end": end_date
        }
        
        try:
            response = requests.get(FRED_BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "observations" not in data:
                print(f"⚠️  警告：{series_id} 無數據")
                return pd.DataFrame()
            
            df = pd.DataFrame(data["observations"])
            df["date"] = pd.to_datetime(df["date"])
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df[["date", "value"]].dropna()
            
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 獲取 {series_id} 失敗: {e}")
            return pd.DataFrame()
    
    def fetch_all_indicators(self) -> Dict[str, pd.DataFrame]:
        """
        獲取所有經濟指標數據
        
        Returns:
            Dict[indicator_name, DataFrame]
        """
        print("📊 開始獲取總體經濟數據...\n")
        
        results = {}
        total = len(ECONOMIC_INDICATORS)
        
        for idx, (indicator_name, indicator_info) in enumerate(ECONOMIC_INDICATORS.items(), 1):
            series_id = indicator_info["series_id"]
            name_zh = indicator_info["name_zh"]
            
            print(f"[{idx}/{total}] 獲取 {name_zh} ({series_id})...", end=" ")
            
            df = self.fetch_series(series_id)
            
            if not df.empty:
                results[indicator_name] = df
                print(f"✅ 成功 ({len(df)} 筆資料)")
            else:
                print("❌ 失敗")
        
        self.data_cache = results
        print(f"\n✅ 完成！成功獲取 {len(results)}/{total} 項指標\n")
        
        return results
    
    def calculate_changes(self, df: pd.DataFrame, periods: List[int] = [1, 12]) -> pd.DataFrame:
        """
        計算變化率 (MoM, YoY 等)
        
        Args:
            df: DataFrame with columns [date, value]
            periods: 計算週期（1=MoM, 12=YoY for monthly data）
            
        Returns:
            DataFrame with additional change columns
        """
        df = df.sort_values("date").copy()
        
        for period in periods:
            df[f"change_{period}"] = df["value"].pct_change(periods=period) * 100
        
        return df
    
    def get_latest_values(self) -> Dict:
        """
        獲取所有指標的最新值
        
        Returns:
            Dict with latest values and changes
        """
        if not self.data_cache:
            print("⚠️  請先執行 fetch_all_indicators()")
            return {}
        
        latest_data = {}
        
        for indicator_name, df in self.data_cache.items():
            if df.empty:
                continue
            
            df_with_changes = self.calculate_changes(df, periods=[1, 12])
            latest_row = df_with_changes.iloc[-1]
            
            indicator_info = ECONOMIC_INDICATORS[indicator_name]
            
            latest_data[indicator_name] = {
                "name": indicator_info["name"],
                "name_zh": indicator_info["name_zh"],
                "date": latest_row["date"].strftime("%Y-%m-%d"),
                "value": round(latest_row["value"], 2),
                "unit": indicator_info["unit"],
                "change_1m": round(latest_row.get("change_1", 0), 2),
                "change_12m": round(latest_row.get("change_12", 0), 2),
                "importance": indicator_info["importance"]
            }
        
        return latest_data
    
    def calculate_yield_curve_spread(self) -> Optional[float]:
        """
        計算殖利率曲線斜率 (10Y - 2Y)
        
        Returns:
            Spread in basis points (bps), or None if data unavailable
        """
        if "10Y_TREASURY" not in self.data_cache or "2Y_TREASURY" not in self.data_cache:
            return None
        
        df_10y = self.data_cache["10Y_TREASURY"]
        df_2y = self.data_cache["2Y_TREASURY"]
        
        if df_10y.empty or df_2y.empty:
            return None
        
        latest_10y = df_10y.iloc[-1]["value"]
        latest_2y = df_2y.iloc[-1]["value"]
        
        spread = latest_10y - latest_2y
        
        return round(spread, 2)
    
    def calculate_real_interest_rate(self) -> Optional[float]:
        """
        計算實質利率 (Fed Funds Rate - Core CPI YoY)
        
        Returns:
            Real interest rate in percent, or None if data unavailable
        """
        if "FED_FUNDS_RATE" not in self.data_cache or "CORE_CPI" not in self.data_cache:
            return None
        
        df_fed = self.data_cache["FED_FUNDS_RATE"]
        df_cpi = self.data_cache["CORE_CPI"]
        
        if df_fed.empty or df_cpi.empty:
            return None
        
        fed_rate = df_fed.iloc[-1]["value"]
        
        # Calculate Core CPI YoY
        df_cpi_with_changes = self.calculate_changes(df_cpi, periods=[12])
        cpi_yoy = df_cpi_with_changes.iloc[-1]["change_12"]
        
        real_rate = fed_rate - cpi_yoy
        
        return round(real_rate, 2)
    
    def generate_summary_report(self) -> Dict:
        """
        生成總結報告
        
        Returns:
            綜合分析報告 Dict
        """
        latest_data = self.get_latest_values()
        yield_spread = self.calculate_yield_curve_spread()
        real_rate = self.calculate_real_interest_rate()
        
        report = {
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_period": f"{self.start_date} to {self.end_date}",
            "yield_curve_spread_10y2y": yield_spread,
            "yield_curve_status": self._interpret_yield_curve(yield_spread),
            "real_interest_rate": real_rate,
            "real_rate_status": self._interpret_real_rate(real_rate),
            "indicators": latest_data,
            "economic_assessment": self._assess_economic_environment(latest_data, yield_spread, real_rate)
        }
        
        return report
    
    def _interpret_yield_curve(self, spread: Optional[float]) -> str:
        """解讀殖利率曲線"""
        if spread is None:
            return "數據不足"
        
        if spread < -0.5:
            return "深度倒掛（衰退警訊）"
        elif spread < 0:
            return "倒掛（經濟放緩）"
        elif spread < 0.5:
            return "平坦化（警戒）"
        elif spread < 2.0:
            return "正常（健康）"
        else:
            return "陡峭化（復甦期）"
    
    def _interpret_real_rate(self, real_rate: Optional[float]) -> str:
        """解讀實質利率"""
        if real_rate is None:
            return "數據不足"
        
        if real_rate > 2.0:
            return "高實質利率（緊縮）"
        elif real_rate > 0:
            return "正實質利率（中性偏緊）"
        elif real_rate > -2.0:
            return "負實質利率（寬鬆）"
        else:
            return "深度負實質利率（極度寬鬆）"
    
    def _assess_economic_environment(self, latest_data: Dict, 
                                    yield_spread: Optional[float], 
                                    real_rate: Optional[float]) -> Dict:
        """
        評估總體經濟環境
        
        Returns:
            經濟環境評估 Dict
        """
        assessment = {
            "economic_cycle": "Unknown",
            "inflation_status": "Unknown",
            "labor_market": "Unknown",
            "policy_stance": "Unknown",
            "risk_level": "Unknown",
            "investment_strategy": "Unknown"
        }
        
        # 判斷經濟週期
        if yield_spread is not None:
            if yield_spread < 0:
                assessment["economic_cycle"] = "衰退風險期"
            elif yield_spread < 1.0:
                assessment["economic_cycle"] = "擴張後期"
            else:
                assessment["economic_cycle"] = "復甦/擴張期"
        
        # 判斷通膨狀況
        if "CORE_CPI" in latest_data:
            cpi_yoy = latest_data["CORE_CPI"]["change_12m"]
            if cpi_yoy > 4.0:
                assessment["inflation_status"] = "高通膨"
            elif cpi_yoy > 3.0:
                assessment["inflation_status"] = "溫和通膨"
            elif cpi_yoy > 2.0:
                assessment["inflation_status"] = "目標區間"
            else:
                assessment["inflation_status"] = "低通膨/通縮風險"
        
        # 判斷就業市場
        if "UNEMPLOYMENT_RATE" in latest_data:
            unemp = latest_data["UNEMPLOYMENT_RATE"]["value"]
            if unemp < 4.0:
                assessment["labor_market"] = "緊俏（過熱風險）"
            elif unemp < 5.0:
                assessment["labor_market"] = "健康"
            else:
                assessment["labor_market"] = "疲弱"
        
        # 判斷政策立場
        if real_rate is not None:
            if real_rate > 1.5:
                assessment["policy_stance"] = "緊縮"
            elif real_rate > 0:
                assessment["policy_stance"] = "中性偏緊"
            elif real_rate > -1.0:
                assessment["policy_stance"] = "中性偏鬆"
            else:
                assessment["policy_stance"] = "寬鬆"
        
        # 綜合風險評估
        risk_factors = 0
        if yield_spread and yield_spread < 0:
            risk_factors += 2
        if "CORE_CPI" in latest_data and latest_data["CORE_CPI"]["change_12m"] > 4.0:
            risk_factors += 1
        if "UNEMPLOYMENT_RATE" in latest_data and latest_data["UNEMPLOYMENT_RATE"]["value"] > 5.0:
            risk_factors += 1
        
        if risk_factors >= 3:
            assessment["risk_level"] = "高風險"
            assessment["investment_strategy"] = "防禦為主，高現金比例"
        elif risk_factors >= 1:
            assessment["risk_level"] = "中等風險"
            assessment["investment_strategy"] = "謹慎樂觀，平衡配置"
        else:
            assessment["risk_level"] = "低風險"
            assessment["investment_strategy"] = "積極配置，聚焦成長"
        
        return assessment
    
    def save_to_json(self, filepath: str):
        """儲存為 JSON 格式"""
        report = self.generate_summary_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON 報告已儲存至: {filepath}")
    
    def save_to_csv(self, output_dir: str):
        """儲存為 CSV 格式（每個指標一個檔案）"""
        if not self.data_cache:
            print("⚠️  無數據可儲存")
            return
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for indicator_name, df in self.data_cache.items():
            if df.empty:
                continue
            
            filepath = os.path.join(output_dir, f"{indicator_name.lower()}.csv")
            df_with_changes = self.calculate_changes(df, periods=[1, 12])
            df_with_changes.to_csv(filepath, index=False)
        
        print(f"✅ CSV 檔案已儲存至: {output_dir}")
    
    def print_summary(self):
        """印出總結報告到終端機"""
        report = self.generate_summary_report()
        
        print("\n" + "="*80)
        print("📊 總體經濟數據總結報告")
        print("="*80)
        print(f"報告時間: {report['report_date']}")
        print(f"數據期間: {report['data_period']}")
        print("="*80)
        
        print("\n【關鍵指標】")
        print(f"  殖利率曲線 (10Y-2Y): {report['yield_curve_spread_10y2y']} bps - {report['yield_curve_status']}")
        print(f"  實質利率: {report['real_interest_rate']}% - {report['real_rate_status']}")
        
        print("\n【經濟環境評估】")
        assessment = report['economic_assessment']
        print(f"  經濟週期: {assessment['economic_cycle']}")
        print(f"  通膨狀況: {assessment['inflation_status']}")
        print(f"  就業市場: {assessment['labor_market']}")
        print(f"  政策立場: {assessment['policy_stance']}")
        print(f"  風險等級: {assessment['risk_level']}")
        print(f"  投資策略: {assessment['investment_strategy']}")
        
        print("\n【核心經濟指標】")
        print(f"{'指標':<30} {'最新值':>12} {'單位':<15} {'MoM%':>8} {'YoY%':>8}")
        print("-"*80)
        
        for indicator_name, data in report['indicators'].items():
            if ECONOMIC_INDICATORS[indicator_name]["importance"] == "⭐⭐⭐":
                print(f"{data['name_zh']:<28} {data['value']:>12.2f} {data['unit'][:13]:<15} "
                      f"{data['change_1m']:>8.2f} {data['change_12m']:>8.2f}")
        
        print("="*80 + "\n")


# ============================================================================
# 主程式
# ============================================================================

def main():
    """主程式進入點"""
    
    parser = argparse.ArgumentParser(
        description="總體經濟數據自動獲取腳本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例用法:
  python fetch_macro_data.py --api-key YOUR_KEY
  python fetch_macro_data.py --api-key YOUR_KEY --output ./data --years 10
  python fetch_macro_data.py --api-key YOUR_KEY --format json --output report.json

注意事項:
  - 需要 FRED API Key (免費申請: https://fred.stlouisfed.org/docs/api/api_key.html)
  - 可使用環境變數 FRED_API_KEY 設定 API Key
  - 預設獲取最近 5 年數據
        """
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="FRED API Key (或使用環境變數 FRED_API_KEY)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./macro_data",
        help="輸出目錄或檔案路徑 (預設: ./macro_data)"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "csv", "both"],
        default="both",
        help="輸出格式 (預設: both)"
    )
    parser.add_argument(
        "--years",
        type=int,
        default=5,
        help="回溯資料年數 (預設: 5)"
    )
    parser.add_argument(
        "--print-summary",
        action="store_true",
        help="印出總結報告到終端機"
    )
    
    args = parser.parse_args()
    
    # 獲取 API Key
    api_key = args.api_key or os.getenv("FRED_API_KEY")
    
    if not api_key:
        print("❌ 錯誤: 未提供 FRED API Key")
        print("請使用 --api-key 參數或設定環境變數 FRED_API_KEY")
        print("\n免費申請: https://fred.stlouisfed.org/docs/api/api_key.html")
        sys.exit(1)
    
    # 初始化 Fetcher
    fetcher = MacroDataFetcher(api_key=api_key, lookback_years=args.years)
    
    # 獲取數據
    fetcher.fetch_all_indicators()
    
    # 輸出結果
    if args.format in ["json", "both"]:
        if args.format == "json":
            output_path = args.output if args.output.endswith(".json") else os.path.join(args.output, "macro_data_report.json")
        else:
            output_path = os.path.join(args.output, "macro_data_report.json")
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fetcher.save_to_json(output_path)
    
    if args.format in ["csv", "both"]:
        csv_dir = args.output if not args.output.endswith(".json") else "./macro_data_csv"
        fetcher.save_to_csv(csv_dir)
    
    # 印出總結
    if args.print_summary or args.format == "both":
        fetcher.print_summary()
    
    print("🎉 完成！")


if __name__ == "__main__":
    main()
