import React, { useState } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

function LineGraph() {
    const options = {
        title: {
            text: 'Total Positions Market Value',
            align: 'left'
        },

        yAxis: {
            title: {
                text: 'Market Value'
            }
        },

        xAxis: {
            accessibility: {
                rangeDescription: 'Range: Jan 2023 to Aug 2023'
            }
        },

        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },

        plotOptions: {
            series: {
                label: {
                    connectorAllowed: false
                },
                pointStart: 1
            }
        },

        series: [{
            name: 'Other',
            data: [43934, 48656, 65165, 81827, 112143, 142383,
                171533, 165174].map((x) => 100 * x)
        }, {
            name: 'Virtous',
            data: [24916, 37941, 29742, 29851, 32490, 30282,
                38121, 31050].map((x) => 100 * x)
        }, {
            name: 'Catalysm',
            data: [11744, 30000, 16005, 19771, 20185, 24377,
                32147, 30912].map((x) => 100 * x)
        }, {
            name: 'Trustmind',
            data: [null, null, null, null,
                null, 11164, 11218, 10077].map((x) => 100 * x)
        }, {
            name: 'Applebead',
            data: [21908, 5548, 8105, 11248, 8989, 11816, 18274,
                17300].map((x) => 100 * x)
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }

    }

    fetch('http://3.0.49.217/instruments/')
        .then(response => response.json())
        .then(data => {
            const series = data.map(item => ({
                name: 'Year ' + item.year,
                data: item.values
            }));
            setData(series); // Assuming setData is a function that accepts the series data
        })
        .catch(error => console.error('Error fetching messages:', error));
    return (
        <div>
            <HighchartsReact
                highcharts={Highcharts}
                options={options}
            />
        </div>
    );
}

export default LineGraph;