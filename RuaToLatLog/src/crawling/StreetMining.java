package crawling;


import java.io.FileReader;
import java.io.FileWriter;
import java.util.HashMap;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;

public class StreetMining {

	
	
	
	public static void main(String[] args) throws Exception {
		
		
		
		try{
			HashMap<String, String> mapa = new HashMap<String, String>();
			String csvFilename = "/home/arthur/Documents/SafeBus2/crimes_considerados2.csv";
			String outputFile = "/home/arthur/Documents/SafeBus2/outPut3.csv";
			CSVReader csvReader = new CSVReader(new FileReader(csvFilename));
			CSVWriter writer = new CSVWriter(new FileWriter(outputFile));
			String[] row = null;
			int count = 0;
			while((row = csvReader.readNext()) != null) {
				String lougadoro = row[12];
				if (!coletar(lougadoro, "campina grande pb").equals("LAT e LONG nao encontradas.")){
					if (count !=0){
						if(!lougadoro.isEmpty()){
							if (!mapa.containsKey(lougadoro)){
								mapa.put(lougadoro, coletar(lougadoro, "campina grande pb"));
							}
							String lat = mapa.get(lougadoro).split(",")[0];
							String longi = mapa.get(lougadoro).split(",")[1];
							
							String[] temp = {lougadoro, lat,longi};
							System.out.println(temp[0] + "/" + temp[1] + "/" + temp[2]);
							writer.writeNext(temp);
							
						}
					}
					count++;
				}
			}
			writer.close();
			csvReader.close();
		}catch (Exception e) {
			System.out.println(e.getMessage());
		
		}
		
		
		
//		String xml = coletar("av floriano peixoto", "campina grande pb");
		
//		System.out.println();
//		System.out.println(">>>");
//		System.out.println(extrairLatLon(xml));
		
	}
	
	
	private static String extrairLatLon(String html) {
		if(html.contains("ZERO_RESULTS")){
			return "LAT e LONG nao encontradas.";
		}
		else{
			String[] location = html.split("<location>");
			System.out.println("Location: "+ location[0]);
			String loc = location[1].split("</location>")[0];
			
			String lat = loc.split("<lat>")[1].split("</lat>")[0];
			String lon = loc.split("<lng>")[1].split("</lng>")[0];
			
			lat = lat.trim();
			lon = lon.trim();
			
			return  lat + "," + lon;
		}
	}




	private static String coletar(String logradouro, String cidade) throws Exception {		
		if (logradouro.isEmpty()){
			return "";
		}
		else{
			if (logradouro.contains("RUA RIO BRANCO")){
				logradouro = "Av. Barão Rio Branco";
			}
			else if(logradouro.contains("RUA MONSENHOR JOSE COUTINHO")){
				logradouro = "Severino Pereira Rodrigues";
			}
			String url = "http://maps.googleapis.com/maps/api/geocode/xml?address=" + logradouro.replace(" ", "+") + "+" + cidade.replace(" ", "+");
			try {
				Document doc = Jsoup.connect(url).get();
				return extrairLatLon(doc.html());
				
			} catch (Exception e) {
				System.out.println("Logradouro: "+logradouro);
				e.printStackTrace();
			}
			
			throw new Exception("Problemas na coleta");
		}
	}

}
