<Query Kind="Program">
  <NuGetReference>CsvHelper</NuGetReference>
  <Namespace>CsvHelper</Namespace>
  <Namespace>CsvHelper.Configuration</Namespace>
  <Namespace>CsvHelper.Configuration.Attributes</Namespace>
  <Namespace>CsvHelper.Expressions</Namespace>
  <Namespace>CsvHelper.TypeConversion</Namespace>
  <Namespace>System.Globalization</Namespace>
</Query>

void Main()
{
	var categoryReader = new StreamReader(@"C:\Users\Ryan\Desktop\ItemCategoryMapping.csv");
	var categoryCsv = new CsvReader(categoryReader, CultureInfo.InvariantCulture);
	var categoryRecords = categoryCsv.GetRecords<CategoryMapping>().ToList();	
	var rx = new Regex(@"[a-zA-Z0-9]*\.", RegexOptions.Compiled | RegexOptions.IgnoreCase);
	var CategoryMap = new Dictionary<Category, List<string>>();
	
	foreach (var record in categoryRecords)
	{
		record.CategoryDescription = rx.Replace(record.CategoryDescription, @"").Trim();
	}
	
	var uniqueDescriptions = categoryRecords.Select(x => x.CategoryDescription).Distinct().ToList();

	foreach (var desc in uniqueDescriptions)
	{
		var catRecord = categoryRecords.FirstOrDefault(x => x.CategoryDescription == desc);
		var category = new Category{
			CategoryDescription = desc,
			CategoryMaxPoints = catRecord.CategoryMaxPoints
		};
		var items = categoryRecords.Where(x => x.CategoryDescription == desc).Select(x=> x.ItemID).ToList();
		
		CategoryMap.Add(category, items);
	}

	Console.WriteLine(CategoryMap.Count());
	var categoryWriter = new StreamWriter(@"C:\Users\Ryan\Desktop\ItemMapping.csv");
	var csvWriter = new CsvWriter(categoryWriter, CultureInfo.InvariantCulture);
	csvWriter.WriteRecords(categoryRecords);
}

// Define other methods, classes and namespaces here


public class CategoryMapping
{
	public string ItemID { get; set; }
	public string CategoryCode { get; set; }
	public string CategoryDescription { get; set; }
	public string CategoryMaxPoints { get; set; }
	
}

public class Category
{
	public string CategoryDescription { get; set; }
	public string CategoryMaxPoints { get; set; }

}