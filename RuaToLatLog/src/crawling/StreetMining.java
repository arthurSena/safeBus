package crawling;


import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class StreetMining {

	
	
	
	public static void main(String[] args) throws Exception {
		
		
		String xml = coletar("av floriano peixoto", "campina grande pb");
		
		System.out.println();
		System.out.println(">>>");
		System.out.println(extrairLatLon(xml));
		
	}
	
	
	private static String extrairLatLon(String html) {
		String[] location = html.split("<location>");
		
		String loc = location[1].split("</location>")[0];
		
		String lat = loc.split("<lat>")[1].split("</lat>")[0];
		String lon = loc.split("<lng>")[1].split("</lng>")[0];
		
		lat = lat.trim();
		lon = lon.trim();
		
		return "(" + lat + "," + lon + ")";
	}




	private static String coletar(String logradouro, String cidade) throws Exception {		
		
		String url = "http://maps.googleapis.com/maps/api/geocode/xml?address=" + logradouro.replace(" ", "+") + "+" + cidade.replace(" ", "+") + "&sensor=false";
		
		try {
			Document doc = Jsoup.connect(url).get();
			
			System.out.println(doc.html());
			
			return doc.html();
			
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		throw new Exception("Problemas na coleta");

	}

}
