class FraudSummaryWidget(Widget):
    async def render(self, request: Request) -> str:
        from models.fraud import Fraud  # Lazy import to avoid circular errors
        reports = await Fraud.all()
        total = len(reports)
        resolved = sum(1 for r in reports if r.status == "resolved")
        pending = sum(1 for r in reports if r.status == "pending")
        flagged = sum(1 for r in reports if r.risk_level == "high")

        template = Template("""
        <div class="p-4 bg-white dark:bg-gray-800 rounded-xl shadow-md mt-6">
          <h2 class="text-lg font-bold text-gray-700 dark:text-white mb-2">Fraud Summary</h2>
          <table class="min-w-full text-sm text-left text-gray-500 dark:text-gray-200">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-200">
              <tr>
                <th class="py-2 px-4">Metric</th>
                <th class="py-2 px-4">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr><td class="py-2 px-4">Total Reports</td><td class="py-2 px-4">{{ total }}</td></tr>
              <tr><td class="py-2 px-4">Resolved Cases</td><td class="py-2 px-4">{{ resolved }}</td></tr>
              <tr><td class="py-2 px-4">Pending Reviews</td><td class="py-2 px-4">{{ pending }}</td></tr>
              <tr><td class="py-2 px-4">High-Risk Flags</td><td class="py-2 px-4">{{ flagged }}</td></tr>
            </tbody>
          </table>
        </div>
        """)

        return template.render(
            total=total,
            resolved=resolved,
            pending=pending,
            flagged=flagged
        )