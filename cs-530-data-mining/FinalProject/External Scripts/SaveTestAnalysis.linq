<Query Kind="Program">
  <Connection>
    <ID>9292f970-a9eb-46c3-9813-8f7e6b58d3b3</ID>
    <NamingServiceVersion>2</NamingServiceVersion>
    <Persist>true</Persist>
    <Driver Assembly="(internal)" PublicKeyToken="no-strong-name">LINQPad.Drivers.EFCore.DynamicDriver</Driver>
    <Server>localhost</Server>
    <Database>TestAnalysis</Database>
    <DriverData>
      <EFProvider>Microsoft.EntityFrameworkCore.SqlServer</EFProvider>
    </DriverData>
  </Connection>
  <Output>DataGrids</Output>
  <Namespace>System.Threading.Tasks</Namespace>
</Query>

void Main()
{
	var startValue = 0; 
	var settings = new XmlReaderSettings();
	settings.ValidationType = ValidationType.None;
	for(var i = 0; i < 2; i++){
		var summaries = TestSummaries.OrderByDescending (t => t.TestStarted).Skip(startValue).Take(1000);
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
					var correct = score.InnerText == "Correct" ? true : false;
					if(correct) totalCorrect++;
					catItem.Correct = true;
				}
				
				categoryItems.Add(catItem);
			}
			
			Parallel.ForEach(categories, (category)=>{
				var categoryItemIds = ItemMappings.Where(x=> x.CategoryDescription == category).Select(x => x.ItemID).ToList();
				var totalCategoryItems = 0;
				var correctCategoryItems = 0;
				if (categoryItemIds.Any())
				{
					var itemsInCategory = categoryItems.Where(x => categoryItemIds.Contains(x.ItemId)).ToList();

					if (itemsInCategory.Any())
					{
						foreach (var item in itemsInCategory)
						{
							totalCategoryItems++;
							if (item.Correct) correctCategoryItems++;
						}
						var mappedCateogry = ItemMappings.FirstOrDefault(x => x.CategoryDescription == category);
						var categoryAnalysis = new TestCategoryAnalysis
						{
							SeriesName = summary.SeriesName,
							Abbreviation = summary.Abbreviation,
							TestName = summary.TestName,
							CategoryDescription = mappedCateogry.CategoryDescription,
							CategoryCode = mappedCateogry.CategoryCode,
							CategoryMaxPoints = mappedCateogry.CategoryMaxPoints,
							CategoryScore = correctCategoryItems,
							CategoryTruePercentage = correctCategoryItems / totalCategoryItems
						};

						TestCategoryAnalysis.Add(categoryAnalysis);
						SaveChanges();
					}
				}

			});
			
			float truePercent = (float)totalCorrect/(float)totalQuestions;
			
			var analysis = new TestSummaryAnalysis{
				SeriesName = summary.SeriesName,
				Abbreviation = summary.Abbreviation,
				TestName = summary.TestName,
				SchoolId = Guid.Parse(summary.SchoolId),
				SchoolStateCode = summary.SchoolStateCode,
				InstructorId = Guid.Parse(summary.InstructorId),
				StudentId = Guid.Parse(summary.StudentId),
				PossibleCheating = summary.PossibleCheating == 1 ? true : false,
				MaxPoints = summary.MaxPoints,
				CutPoints = summary.CutPoints,
				QuestionsAnswered = summary.QuestionsAnswered,
				QuestionsDelivered = summary.QuestionsDelivered,
				PassFail = summary.PassFail,
				TestStarted = DateTime.Parse(summary.TestStarted),
				TestCompleted = DateTime.Parse(summary.TestCompleted),
				ScorePercentage = summary.ScorePercentage,
				TruePercentage = truePercent,
				TestScore = summary.TestScore				
			};
			TestSummaryAnalysis.Add(analysis);
		}
		SaveChanges();
		startValue = i*1000+1;
	}

}

public class Item{
	public string ItemId {get;set;}
	public bool Correct {get;set;}
}


// Define other methods, classes and namespaces here