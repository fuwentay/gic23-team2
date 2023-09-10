// @mui material components
import React, { useState } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

function BarChart() {
    const options = {
        chart: {
            type: 'bar'
        },
        title: {
            text:""
        },
        subtitle: {
            text: '',
            align: 'left'
        },
        xAxis: {
            categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
            title: {
                text: null
            },
            gridLineWidth: 1,
            lineWidth: 0
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Population (millions)',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            },
            gridLineWidth: 0
        },
        tooltip: {
            valueSuffix: ' millions'
        },
        plotOptions: {
            bar: {
                borderRadius: '50%',
                dataLabels: {
                    enabled: true
                },
                groupPadding: 0.1
            }
        },

        credits: {
            enabled: false
        },
        series: [{
            name: 'Year 1990',
            data: [631, 727, 3202, 721, 26]
        }, {
            name: 'Year 2000',
            data: [814, 841, 3714, 726, 31]
        }, {
            name: 'Year 2010',
            data: [1044, 944, 4170, 735, 40]
        },]
    };


    fetch('/instruments/')
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

export default BarChart;