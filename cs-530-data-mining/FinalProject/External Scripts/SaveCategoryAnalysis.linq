<Query Kind="Program">
  <Connection>
    <ID>ecbcf036-335c-4d5e-bb86-12ede3690c08</ID>
    <NamingServiceVersion>2</NamingServiceVersion>
    <Persist>true</Persist>
    <Server>127.0.0.1</Server>
    <Database>TestAnalysis</Database>
    <DriverData>
      <ExtraCxOptions>MultipleActiveResultSets=true</ExtraCxOptions>
    </DriverData>
  </Connection>
  <Output>DataGrids</Output>
  <Namespace>System.Threading.Tasks</Namespace>
</Query>

async void Main()
{
	var startValue = 0; 
	var settings = new XmlReaderSettings();
	settings.ValidationType = ValidationType.None;
	var startingSummaryId = 0;
	var count = 0;
	for(var i = 0; i < 2; i++){
	
		var summaries = TestSummaries.OrderByDescending (t => t.TestStarted).Skip(startValue).Take(1000).ToList();
		var categories = ItemMappings.Select(x => x.CategoryDescription).Distinct().ToList();
		
		foreach (var summary in summaries)
		{	
			var totalQuestions = 0;
			var totalCorrect = 0;
			var categoryItems = new List<Item>();
			var data = summary.ResponseData.ToString();
			var reader = XmlReader.Create(new StringReader(data), settings);
			
			XmlDocument xmlDoc = new XmlDocument();
			xmlDoc.Load(reader);
			XmlNodeList elemList = xmlDoc.SelectNodes("//presentation/item[1]");
			
			foreach (XmlNode element in elemList){
				totalQuestions++;
				var itemId = element.Attributes["id"].Value;
				var score = element.SelectSingleNode("score");
				
				var catItem = new Item
				{
					ItemId = itemId,
					Correct = false
				};
				
				if(score != null){
					var correct = score.InnerText == "1" ? true : false;
					if(correct) totalCorrect++;
					catItem.Correct = true;
				}
				
				categoryItems.Add(catItem);
			}
			var testItems = new List<TestItemAnalysis>();
			foreach (var item in categoryItems)
			{
				var mappedCateogry = ItemMappings.FirstOrDefault(x=> x.ItemID == item.ItemId);
				var itemAnalysis = new TestItemAnalysis
				{
					TestSummaryId = startingSummaryId,
					ItemId = item.ItemId,
					ItemCorrect =	item.Correct,
					CategoryDescription = mappedCateogry.CategoryDescription,
					CategoryCode = mappedCateogry.CategoryCode
				};
				testItems.Add(itemAnalysis);
				count++;
			}
			TestItemAnalysis.InsertAllOnSubmit(testItems);
			SubmitChanges();
			
			startingSummaryId++;
			Console.WriteLine($"Current Total {count}");
		}
		startValue = i * 1000 + 1;

	}
	Console.Write(count);
}

public class Item{
	public string ItemId {get;set;}
	public bool Correct {get;set;}
}


// Define other methods, classes and namespaces here