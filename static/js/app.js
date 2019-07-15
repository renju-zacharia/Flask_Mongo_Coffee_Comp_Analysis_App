   // Plot Tweets Count and publish in tweets div 
function buildTweets(company) {

    console.log(`Company Selected in buildTweets : ` + company); 
  
    url=`/tweets/`+company;
  
    console.log(url);
  
    d3.json(url).then(function(data){
  
      // console.log(data);
        
      var data2 = [{
        x: data["sentiments"],
        y: data["ratings"], 
        hovertext: data["company"],                
        'marker': {
          'color': [
            'rgb(0, 204, 0)',    // green
            'rgb(11, 133, 215)', // light blue
            'rgb(215, 11, 11)'   // red                   
            ]
        },
        type: "bar"
      }];
    
      var layout2={ title: '<b>Bar Chart - </b> Sentiments'};
    
      Plotly.newPlot('tweets', data2, layout2); 
  
  });
}

   // Plot Tweets Count and publish in tweets div 
function buildReTweets(company) {

    console.log(`Company Selected in buildReTweets : ` + company); 
  
    url=`/retweets/`+company;
  
    console.log(url);
  
    d3.json(url).then(function(data){
  
      // console.log(data);
        
      // var data2 = [{
      //   x: data["sentiments"],
      //   y: data["retweets"], 
      //   hovertext: data["company"],
      //   type: "bar"
      // }];
    
      // var layout2={ title: '<b>Bar Chart - </b> Retweets'};

      var data2 = [{
        values: data["retweets"],       
        labels: data["sentiments"],
        hovertext: data["company"],        
        'marker': {
          'colors': [
            'rgb(0, 204, 0)',    // green
            'rgb(11, 133, 215)', // light blue
            'rgb(215, 11, 11)'   // red            
            ]
        },
        type: "pie"
      }];
    
      var layout2={ title: '<b>Pie Chart - </b> Retweets'};
      
      Plotly.newPlot('retweets', data2, layout2); 

  });
}
  // Get Sample Tweets and disply on dashboard
function buildMetadata(company) {

      // console.log(`Company Selected in buildMetadata : ` + company); 

      url=`/metadata/`+company;

      if (company == "SB"){
          v_company = "Starbucks"
      }
      else if (company == "MD") {
          v_company = "McDonald's"
      }
      else if (company == "DD"){
          v_company = "Dunkin Donuts"
      }
      
      console.log(url);
  
      var metadata = d3.select('#recent-tweets');

      d3.json(url).then(function(data){
        
        d3.select('#company-head').selectAll("h3").remove();
        d3.select('#company-head').append("h3").text(v_company);

        d3.select('#recent-tweets').selectAll("h5").remove();  
        Object.entries(data).forEach(([key, value]) =>  d3.select('#recent-tweets').append("h5").text( key + ' : ' + value ) );
  
      });  
  
  }

 // Plot Rating Counts and publish in rating div 
function buildRating(company) {
  
    console.log(`Company Selected in buildRating : ` + company); 
  
    url=`/rating/`+company;

    console.log(url);
  
    d3.json(url).then(function(data){
  
      // console.log(data);
        
      var data2 = [{
        values: data["ratings"],       
        labels: data["sentiments"],
        hovertext: data["company"],
        'marker': {
          'colors': [
            'rgb(0, 204, 0)',    // green
            'rgb(11, 133, 215)', // light blue
            'rgb(215, 11, 11)'   // red         
            ]
        },
        type: "pie"
      }];
    
      var layout2={ title: '<b>Pie Chart - </b> Sentiments'};
    
      Plotly.newPlot('rating', data2, layout2); 
      
  }); 
  
  }
  
// Plot Stores Counts and Revenues
function buildStores(company) {

    url=`/sales/`+company;

    d3.json(url).then(function(data){

      // Bubble Chart
      var trace1 = {
        x: data['year'],
        y: data['stores'],
        mode: 'markers',
        marker: {
            size: data['stores'].map(function(point){
              return parseFloat(point)/150}),
            color: data['stores']
            }
      };

      var data1 = [trace1];

      var layout = {
        title: "US Stores",
        xaxis: { title: "Year"},
        yaxis: { title: "Number of US Stores"},
        showlegend: false,
        height: 600,
        width: 600
      };

      Plotly.newPlot("stores", data1, layout);

      // Bar Chart

      var trace2 = {
        x: data['year'],
        y: data['revenue'],
        type: "bar"
      };

      var data2 = [trace2];

      var layout1 = {
        title: "US Revenues",
        xaxis: { title: "Year"},
        yaxis: { title: "Revenue in Millions of Dollars"}
      };

      Plotly.newPlot("sales", data2, layout1);
    });

}

function buildGauge(company) {

  console.log(`Retweet Count Gauge : ` + company); 

  url=`/retwtcnt/`+company;

  console.log(url);

  d3.json(url).then(function(data){

    console.log(`Gauge Data Num of Retweet : ` + data["retweet_count"]);

    var level = data["retweet_count"] / 100000;
    
    // Trig to calc meter point
    var degrees = 10 - level,
        radius = .5;
    var radians = degrees * Math.PI / 10;
    var x = radius * Math.cos(radians);
    var y = radius * Math.sin(radians);

    // Path: may have to change to create a better triangle
    var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
        pathX = String(x),
        space = ' ',
          pathY = String(y),
      pathEnd = ' Z';

    var path = mainPath.concat(pathX,space,pathY,pathEnd);

    var data3 = [{ type: 'scatter',
      x: [0], y:[0],
      marker: {size: 28, color:'850000'},
        showlegend: false,
        name: 'Retweet Counts : ',
        text: data["retweet_count"],
        hoverinfo: 'name+text'},
        { values: [50/10, 50/10, 50/10, 50/10, 50/10, 50/10, 50/10, 50/10, 50/10, 50/10,50],
        
        rotation: 90,
        text: ['9-10', '8-9','7-8','6-7','5-6','4-5','3-4','2-3','1-2','0-1',''],
        textinfo: 'text',
        textposition:'inside',
        marker: {colors:[
                        'rgba(14, 127, 0, .5)', 
                        'rgba(20, 130, 8, .5)',
                        'rgba(30, 140, 15, .5)',
                        'rgba(70, 145, 20, .5)',
                        'rgba(110, 154, 22, .5)',
                        'rgba(170, 202, 42, .5)', 
                        'rgba(202, 206, 95, .5)',
                        'rgba(210, 209, 145, .5)',
                        'rgba(232, 215, 175, .5)',
                        'rgba(255, 230, 210, .5)',
                        'rgba(255, 255, 255, 0)'
                        ]
                },
        labels: ['9-10', '8-9','7-8','6-7','5-6','4-5','3-4','2-3','1-2','0-1',''],
        hoverinfo: 'label',
        hole: .5,
        type: 'pie',
        showlegend: false
  }];

      var layout3 = {
        shapes:[{
            type: 'path',
            path: path,
            fillcolor: '850000',
            line: {
              color: '850000'
            }
          }],
        title: '<b>Gauge</b> <br> Retweets 0-10 in 100,000s',
        height: 550,
        width: 550,
        xaxis: {zeroline:false, showticklabels:false,
                  showgrid: false, range: [-1, 1]},
        yaxis: {zeroline:false, showticklabels:false,
                  showgrid: false, range: [-1, 1]}
      };

  Plotly.newPlot('gauge', data3, layout3);

}); 

}
  
  function init() {

    console.log('In Init');
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");
  
    var companies = [ 
                      {"company" : "SB" },  
                      {"company" : "MD" }, 
                      {"company" : "DD" }
                    ] 
             
    var arrayLength = companies.length;

    for (var i = 0; i < arrayLength; i++) {
        console.log(companies[i].company);
        //Populate Dropdown with company names
                    selector
                     .append("option")
                     .text(companies[i].company)
                     .property("value", companies[i].company);
            
        }                

      // Use the first Company (Starbucks) from the list to build the initial plots
      const firstSample = companies[0].company;      
      buildTweets(firstSample);
      buildReTweets(firstSample);
      buildGauge(firstSample);
      buildMetadata(firstSample);
      buildRating(firstSample);
      buildStores(firstSample);
  }
  
  function optionChanged(newSample) {
//     // Fetch new data each time a new sample is selected      
      buildTweets(newSample);
      buildReTweets(newSample);
      buildGauge(newSample);
      buildMetadata(newSample);
      buildRating(newSample);
      buildStores(newSample);
  }
  
  // Initialize the dashboard
  init();
  