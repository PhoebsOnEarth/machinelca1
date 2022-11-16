using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using RegressionCA.Models;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using Newtonsoft.Json;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace RegressionCA.Controllers;

public class HomeController : Controller
{
    string Baseurl = "http://localhost:3000/";

    private readonly ILogger<HomeController> _logger;
    public HomeController(ILogger<HomeController> logger)
    {
        _logger = logger;
    }

    public IActionResult Index(string model)
    {
        if (model == "log")
            return View("Log");
        if (model == "time")
            return View("time");
        return View();
    }


    
    public async Task<ActionResult> Log(double x, double y, double w, double z)
    {
        Log log = new Log();
        Console.WriteLine(x);
        using (var client = new HttpClient())
        {
            client.BaseAddress = new Uri(Baseurl);
            client.DefaultRequestHeaders.Clear();
            string request = String.Format("logReg?x={0:0.0}&y={1:0.0}&w={2:0.0}&z={3:0.0}",x,y,w,z);
            ViewBag.request = Baseurl + request;
            HttpResponseMessage Res = await client.GetAsync(request);
            if (Res.IsSuccessStatusCode)
            {
                var response = Res.Content.ReadAsStringAsync().Result;
                log = JsonConvert.DeserializeObject<Log>(response);
            }
            return View(log);
        }
        
    }

    public async Task<ActionResult> Time(int x)
    {
        Time time = new Time();
        using (var client = new HttpClient())
        {
            client.BaseAddress = new Uri(Baseurl);
            client.DefaultRequestHeaders.Clear();
            string request = String.Format("timeSeries?x={0}",x);
            ViewBag.request = Baseurl + request;
            HttpResponseMessage Res = await client.GetAsync(request);
            if (Res.IsSuccessStatusCode)
            {
                var response = Res.Content.ReadAsStringAsync().Result;
                time = JsonConvert.DeserializeObject<Time>(response);
            }
            return View(time);
        }
    }

    

    public IActionResult Privacy()
    {
        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}

