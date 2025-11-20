from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup


def get_promotions(promotion_div):
    """
    Extracts promotion data from Selenium WebElement

    Args:
        promotion_div: Selenium WebElement representing the promotion div

    Returns:
        dict: Dictionary with link data and span texts
    """
    if not promotion_div:
        return None

    # Uzimamo sve span elemente unutar promotion_div
    all_spans = promotion_div.find_elements(By.TAG_NAME, "span")
    # print(all_spans)
    # Proveravamo da li ima barem 4 span elementa
    if len(all_spans) < 4:
        return None

    # Prvi span - uzimamo link i tekst
    first_span = all_spans[0]
    try:
        link_element = first_span.find_element(By.TAG_NAME, "a")
        href = link_element.get_attribute("href")
        link_text = link_element.get_attribute("textContent").strip()


    except:
        href = ''
        link_text = ''

    # Četvrti span - uzimamo tekst
    fourth_span = all_spans[3]
    fourth_span_text = fourth_span.get_attribute("textContent").strip()
    return {
        'link': href,
        'text': link_text,
        'time': fourth_span_text,
    }

def get_geography_data(geography_div):
    """
    Extracts geography data from Selenium WebElement

    Args:
        geography_div: Selenium WebElement representing the geography div

    Returns:
        dict: Dictionary with link data and span texts
    """
    if not geography_div:
        return None

    # Uzimamo sve span elemente unutar geography_div
    all_spans = geography_div.find_elements(By.TAG_NAME, "span")

    # Proveravamo da li ima barem 6 span elemenata
    if len(all_spans) < 6:
        return None

    # Prvi span - uzimamo tekst (MMA)
    first_span = all_spans[0]
    first_span_text = first_span.text.strip()
    if first_span_text != 'MMA':
        return None

    # Treći span - uzimamo tekst (San Antonio, TX / San Antonio)
    third_span = all_spans[2]
    third_span_text = third_span.text.strip()

    # Šesti span - uzimamo link i tekst
    sixth_span = all_spans[5]
    try:
        link_element = sixth_span.find_element(By.TAG_NAME, "a")
        href = link_element.get_attribute("href")
        link_text = link_element.text.strip()
    except:
        href = ''
        link_text = ''

    return {
        'sport_text': first_span_text,
        'location_text': third_span_text,
        'link_href': href,
        'link_text': link_text
    }

def get_event_data_requests(fight_link):
    """
    Extracts event data using requests library instead of Selenium

    Args:
        fight_link: URL of the event page

    Returns:
        dict: Dictionary with event data
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(fight_link, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Ostatak koda je isti kao u prethodnoj funkciji
        list_element = soup.select_one("ul[data-controller='unordered-list-background']")

        if not list_element:
            return None

        list_items = list_element.find_all('li')
        event_data = {}

        for item in list_items:
            spans = item.find_all('span')

            if len(spans) >= 2:
                key = spans[0].get_text().strip().replace(":", "")
                value = spans[1].get_text().strip()

                link = spans[1].find('a')
                if link:
                    event_data[f"{key.lower().replace(' ', '_')}_link"] = link.get('href')

                event_data[key.lower().replace(' ', '_')] = value

        fights = process_fight_card_section(soup)
        event_data['fights'] = fights
        event_data['cancelled'] = cancelled_fight(soup)

        return event_data

    except Exception as e:
        print(f"Greška pri ekstrakciji podataka sa event stranice: {e}")
        return None

def all_fight_data(divs):
    try:
        fighters = divs.find_all('div', class_='div flex flex-col w-[37%] md:w-auto')

        try:
            left_fight = fighters[0]
            is_enter_result = left_fight.find_all(class_='from-[ffffff]') is None
            left_fight_result = left_fight.find('span', class_='text-red-100').get_text() if left_fight.find('span', class_='text-red-100') else ""
            left_fight_img = left_fight.find('img')['src']
            left_fight_a = left_fight.find('a')
            left_fight_name = {
                'success': True,
                'result': left_fight_result,
                'image': left_fight_img,
                'name': left_fight_a.get_text(strip=True),
                'link': left_fight_a.get('href'),
                'process': process_data(left_fight),
                'result_status': is_enter_result
            }
        except Exception as e:
            left_fight_name = {
                'success': False,
                'error': f"Greška u left_fight_name: {str(e)} "
            }

        # sum_fight = fight_sum_divs[1]

        try:
            right_fight = fighters[1]
            is_enter_result = right_fight.find_all(class_='from-[ffffff]') is None
            right_fight_result = right_fight.find('span', class_='text-green-100').get_text() if right_fight.find('span', class_='text-green-100') else ""
            right_fight_img = right_fight.find('img')['src']
            right_fight_a = right_fight.find('a')
            right_fight_name = {
                'success': True,
                'result': right_fight_result,
                'image': right_fight_img,
                'name': right_fight_a.get_text(strip=True),
                'link': right_fight_a.get('href'),
                'process': process_data(right_fight),
                'result_status': is_enter_result
            }
        except Exception as e:
            right_fight_name = {
                'success': False,
                'error': f"Greška u right_fight_name: {str(e)}"
            }

        # right_fight_position_wrap = right_fight.find('div', class_='div flex flex-col md:flex-row items-center')
        # right_fight_position_spans = right_fight_position_wrap.find_all('span')
        # right_fight_position = {
        #     's': right_fight_position_spans[0].get_text().strip(),
        #     'n': right_fight_position_spans[2].get_text().strip()
        # }

        return {
            'success': True,
            'fighter_left': left_fight_name,
            'fight_center': {},
            'fighter_right': right_fight_name
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Greška u all_fight_data: {str(e)}",
        }

def process_fight_card_section(soup_element):
    """
    Procesira div sa ID sectionFightCard i prikuplja sve LI elemente iz UL liste

    Args:
        soup_element: BeautifulSoup element sa kojim treba raditi

    Returns:
        list: Lista svih LI elementa pronadjenih u UL unutar sectionFightCard
    """
    try:
        # Pronađi div sa ID sectionFightCard
        section_div = soup_element.find('div', id='sectionFightCard')

        output = []
        if not section_div:
            print("Nije pronadjen div sa ID 'sectionFightCard'")
            return output

        # Pronađi UL element unutar sectionFightCard
        ul_element = section_div.find('ul')

        if not ul_element:
            print("Nije pronadjen UL element unutar sectionFightCard")
            return output

        # Prikupi sve LI elemente iz UL
        li_elements = ul_element.find_all('li')

        for element in li_elements:
            # Pronalazak target div-a
            target_div = element.find('div', {'data-event-bout-details-target': 'content'})

            result = {}
            if target_div:
                # Prvi div - tekst
                first_div = target_div.find('div')
                competition_type = ''
                if first_div:
                    competition_type = first_div.get_text(strip=True)
                    result['competition_type'] = competition_type

                if competition_type != 'Professional MMA':
                    continue

                # Link
                link_tag = target_div.find('a')
                if link_tag:
                    link_text = link_tag.get_text(strip=True)
                    link_href = link_tag.get('href')
                    result['link'] = {
                        'url': link_href,
                        'text': link_text
                    }

            try:
                # get from event
                wrapper = element.find('div', {'data-bout-wrapper': ''})
                if wrapper:

                    wrapper_divs = wrapper.find_all('div')
                    if wrapper_divs:  # Provera da li ima div elemenata
                        # ISPRAVKA: find_all umesto fint_all
                        win_method_spans = wrapper_divs[0].find_all('span')

                        # Provera da li ima dovoljno span elemenata
                        if len(win_method_spans) >= 3:
                            final_end = {
                                "type": win_method_spans[0].get_text().strip(),
                                "win_method": win_method_spans[1].get_text().strip(),
                                "round": win_method_spans[2].get_text().strip()
                            }
                            result['final'] = final_end
                        else:
                            result['final'] = {}

                        fight_data = wrapper.find('div', class_="div group flex items:start justify-center gap-0.5 md:gap-0")
                        sum_final = all_fight_data(fight_data)
                        result['sum'] = sum_final

                    else:
                        print("Nema div elemenata u wrapper-u")
                        result['final'] = {}
                else:
                    result['final'] = {}

            except Exception as e:
                print(f"Došlo je do greške prilikom obrade final end rezultata: {e}")
                result['final'] = {}


            output.append(result)
        print(f"Pronadjeno {len(li_elements)} LI elementa")

        return output

    except Exception as e:
        print(f"Došlo je do greške: {e}")
        return []

def process_data(fight):
    try:
        div_element = fight.find('div', class_='div flex flex-col md:flex-row items-center')

        if not div_element:
            return []  # Vraća praznu listu umesto greške

        spans = div_element.find_all('span')
        process = [span.text.strip() for span in spans if span.text.strip()]

        return process

    except Exception as e:
        print(f"Greška u procesiranju: {e}")
        return []  # Vraća praznu listu u slučaju greške


def cancelled_fight(soup):
    divs = soup.find_all('div',
                         class_='div flex flex-col w-full pt-4 pb-1.5 md:py-1.5 gap-1 border-b border-dotted border-tap_6')
    fights = []  # Lista za sve borbe

    for div in divs:
        try:
            left_temp = {"success": False, "link": None, "text": None}
            right_temp = {"success": False, "link": None, "text": None}

            left = div.find('div', id='leftNdesktop')
            if left:
                link = left.find('a')
                if link:
                    left_temp = {
                        "success": True,
                        "link": link.get('href'),
                        "text": link.text.strip()
                    }

            right = div.find('div', id='rightNdesktop')
            if right:
                link = right.find('a')
                if link:
                    right_temp = {
                        "success": True,
                        "link": link.get('href'),
                        "text": link.text.strip()
                    }

            # Dodaj borbu u listu umesto return
            fights.append({
                'left': left_temp,
                'right': right_temp
            })

        except Exception as e:
            # Dodaj borbu sa greškom u listu
            fights.append({
                'left': {"success": False, "error": str(e), "link": None, "text": None},
                'right': {"success": False, "error": str(e), "link": None, "text": None}
            })

    return fights  # Vrati listu svih borbi