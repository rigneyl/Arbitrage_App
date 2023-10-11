document.getElementById('searchBtn').addEventListener('click', function() {
    // Fetch opportunities from Flask server and add to HTML
    fetch('/get_opportunities')
        .then(response => response.json())
        .then(data => {
            const opportunityList = document.getElementById('opportunityList');
            opportunityList.innerHTML = ""; // Clear any existing items
            data.opportunities.forEach((opportunity, index) => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <p>${opportunity.message}</p>
                    <p class="profit">Potential Profit: $${opportunity.profit.toFixed(2)}</p>
                    <button onclick="takeTrade(${index})">Take Trade</button>
                `;
                opportunityList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching opportunities:', error);
        });
});

let ledger = [];
let totalProfit = 0;

function takeTrade(index) {
    fetch('/get_opportunities')
        .then(response => response.json())
        .then(data => {
            const opportunity = data.opportunities[index];
            ledger.push(opportunity);
            totalProfit += opportunity.profit;
            updateLedgerDisplay();
        })
        .catch(error => {
            console.error('Error fetching opportunities:', error);
        });
}

function updateLedgerDisplay() {
    const ledgerDisplay = document.getElementById('ledger');
    const totalProfitDisplay = document.getElementById('totalProfit');
    
    ledgerDisplay.innerHTML = ledger.map(trade => `
        <li>
            <p>${trade.message}</p>
            <p class="profit">Profit: $${trade.profit.toFixed(2)}</p>
        </li>
    `).join('');
    
    totalProfitDisplay.innerText = `Total Profit: $${totalProfit.toFixed(2)}`;
}
