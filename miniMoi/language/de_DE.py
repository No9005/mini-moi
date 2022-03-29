"""
The german language files

"""

mapping = {
    'error_codes':{
        'noCommit':"Prozess 'commit' nicht durchführbar.: {e}: {m}.",
        'unableOperation':(
            "Die Operation '{operation}' kann nicht auf/an {element} "
            "ausgeführt werden.: {c}: {e}: {m}."
        ),
        'wrongCategory':(
            "Die ausgewählte Kategorie ist für dieses Product nicht verfügbar. "
            "(vorher '{prior}', jetzt '{p}', Kategorie '{c}')."
        ),
        'wrongProduct':(
            "Ausgewähltes Produkt ist nicht verfügbar."
        ),
        'wrongSubcategory':(
            "Ausgewählte Subkategorie nicht verfügbar."
        ),
        'noEntry':"Sie haben nichts geändert bzw. eingegeben.",
        'notFound':"'{element}' wurde nicht gefunden.",
        'notFoundWithId':"'{element}' wurde nicht gefunden (id = '{id}').",
        'noElementInDB':(
            "Es gibt keine Einträge für '{element}' in der Datenbank. "
            "Bitte fügen Sie zuerst welche hinzu."
        ),
        'noDelivery':"Für morgen gibt es keine Lieferaufträge.",
        'wrongFilter':"Der ausgewählte Filter muss einer der folgenden sein: {f}",
        'uknownFilter':"Der ausgewählte Filter ist unbekannt.",
        'wrongType':"'{var}' muss vom Typ {dtype} sein.",
        'wrongFormat':"'{var}' muss in dem Format '{format}' sein.",
        'notAllowed':"'{var}' muss eines der folgenden Optionen '{available}' sein.",
        'weekdays':"Montag, Dienstag, Mittwoch, Donnerstag, Freitag, Samstag, Sonntag",
        'cycleMismatch':(
            "Es ist nicht erlaubt das '{interval}' leer zu lassen, sollte der '{cycle_type}' "
            "'{day}' oder '{interval_value}' sein."
        ),
        'nextDeliveryMismatch':(
            "Es ist nicht erlaubt die '{next_delivery}' leer zu lassen, wenn "
            "der '{cycle_type}' {none} ist."
            ),
        'missingData':"Folgende Daten fehlen: {column}",
        'defaultProtection':"'Standardwerte' können nicht gelöscht werden.",
        'notUnique':"Ihre Einträge für {table} waren nicht einzigartig: {nonUnique}.",
        'blueprintUnkonwn':"Die ausgewählte Blaupause ist nicht bekannt ('{blueprint}'.",
        'noBlueprintFound':"Es gab keine Blaupausen zum importieren. Bitte erzeugen Sie zuerst eines.",
        'wrongFileType':"Nur Dateien mit Endung '.{format}' sind erlaubt.",
        'pageRefresh':"Bitte aktualisieren Sie die Seite.",
        '500':"Es trat ein Fehler auf: {c}: {m}",
        '404':"Seite '{ressource}' nicht gefunden.",
    },
    'xlsx':{
        'title_overview':"Bestellungen für {date} - {day}",
        'title_details':"Bestelldetails für {date} - {day}",
        'notes':"Notiz:",
        'km':"Kilometer",
        'time':"Zeit",
        'total':"Total",
        'start':"Start",
        'end':"Ende",
        'product_name':"Name",
        'total':"Total",
        'quantity':"Qnt.",
        'category_name':"Kategorie",
        'days':{
            0:"Montag",
            1:"Dienstag",
            2:"Mittwoch",
            3:"Donnerstag",
            4:"Freitag",
            5:"Samstag",
            6:"Sonntag"
        },
        'customer_street':"Straße",
        'customer_nr':"Nr.",
        'customer_name':"Name",
        'customer_surname':"Nachname",
        'product_name':"Produkt",
        'subcategory_name':"Type",
        'cost':'Kosten',
        'total_cost':"Total",
        'customer_phone':"Tel.",
        'customer_mobile':"Mobile",
        'customer_notes':"Notiz",
        'checkbox':"Check",
        'customer_approach':"Anfahrt",
        'customer_town':"Ort",
        'product_selling_price':"Verkaufspreis",
        'product_id':"Produkt id",
        'customer_id':"Konsumenten id",
        'id':"Abo"
    },
    'html_text':{
        'base_html':{
            'site_content':"mini-moi app",
            'base_app_name':"Mini Moi",
            'base_delivery':"Lieferungen",
            'base_tables':"Management",
            'base_reporting':"Report",
            'base_settings':"Einstellungen",
            'base_shutdown':"Beenden",
            'base_documentation':"Dokumentation",
            'base_update':"Updates",
            'base_releases':"Neueste Version",
            'base_version':"Version"
        },
        '/settings':{
            'settings_title':"Einstellungen",
            'settings_lead':"Stellen Sie die App nach Ihren wünschen ein.",
            'settings_language':"Sprache",
            'settings_language_description':"Stellen Sie die App Sprache ein.",
            'settings_logging':"Logging",
            'settings_logging_description':(
                "Diese Option aktiviert das Loggen von Aktionen, "
                "welche vom Nutzer ausgeführt wurden. <br>"
                "<span class='text-danger'>Deaktivierung NICHT empfohlen!</span>"
                ),
            'settings_logging_on':"Aktiviert",
            'settings_logging_off':"Deaktiviert",
            'settings_db_backup':"Datenbank Backup",
            'settings_db_backup_description':(
                "Sie sollten in <b>regelmäßigen Abständen</b> backups Ihrer "
                "Datenbank erstellen. <br>"
                "Mit dem Knopf etwas weiter unten, können Sie eine Kopie der "
                "aktuellen Datenbank erzeugen. <br>"
                "Die Kopie wird abgespeichert in: <br>"
                "<br>"
                "<span class='text-muted'> ~/mini-moi/</span>"
            ),
            'settings_make_backup':"Durchführen",
            'settings_backup_rollback':"Datenbank wiederherstellen",
            'settings_db_rollback':"Datenbank wiederherstellen",
            'settings_db_rollback_description':(
                "Manchmal müssen Sie zu einem vorherigen Datenbank "
                "Zustand zurückkehren. <br>"
                "In diesem Fall können Sie die 'Wiederherstellen' "
                "Funktion verwenden. <br>"
                "Bitte nutzen Sie diese mit äußerster Vorsicht! "
                "Sobald Sie einen alten Stand zurückladen, wird der "
                "aktuelle Stand der Datenbank gelöscht! <br>"
                "<span class='text-muted'><small>Bitte stellen Sie sicher, "
                "dass Sie eine Datenbank Datei ('.db') aus Ihrem 'mini-moi' "
                "Ordner auswählen! <br>"
                "( zu finden unter <b>~/mini-moi/backups/</b> ) </small></span>"
            ),
            'settings_apply_button':"Einstellungen anwenden"
        },
        '/':{
            'index_title':"Startseite",
            'index_hello':"Wilkommen, <b>Mini Moi</b> Nutzer!",
            'index_lead':(
                "Ihr kleiner Assistent zur Übersicht der nächsten Tageslieferungen."
            ),
            'index_getting_started':"Schnellstart",
            'index_steps':"Nur 3 Schritte nötig.",
            'index_setup':"App einrichten ",
            'index_setup_link':"(Hier)",
            'index_enter_data':(
                "Daten einpflegen. <br>"
                "Folgende Daten werden gebraucht:"
                ),
            'index_data_customer':(
                "Konsumentendaten in die <span class='text-info'>Konsumenten Tabelle</span> eintragen."
                ),
            'index_data_categories':(
                "Angabe in der <span class='text-info'>Kategorie</span> & "
                "<span class='text-info'>Subkategorie Tabelle</span> über Produkt die Kategorien "
                "und Subkategorien (optional; z.B. 'Geschnitten', 'Ganz', etc.)."
                
                ),
            'index_data_products':(
                "Die Beschreibung Ihres Produktsortiments in der <span class='text-info'>"
                "Produkt Tabelle</span>"
                ),
            'index_data_abos':(
                "Zu guter Letzt: die Abos Ihrer Konsumenten (<span class='text-info'>Abo Tabelle</span>)"
                ),
            'index_create_report':"Bestellübersicht für den nächsten Tag erstellen ('Lieferungen')!"
        },
        '/shutdown/app':{
            'shutdown_title':"App beendet",
            'shutdown_bye':"Aufwiedersehen, Nutzer!",
            'shutdown_lead':"Auf ein balidges Wiedersehen bei den nächsten Lieferungen &#128513"
        },
        '/delivery':{
            'delivery_title':"Lieferungen",
            'delivery_lead':"Erstellen Sie die Bestellübersicht für den nächsten Tag.",
            'delivery_create_report':"Erstellen",
            'delivery_download':"Übersicht downloaden",
            'delivery_book':"Buchen",
            'delivery_create_tooltip':(
                "Erzeugt die Übersicht für den nächsten Tag. Das Ergebnis wird unten "
                "angezeigt. Sie können anschließend die Übersicht bearbeiten. "
                ),
            'delivery_book_tooltip':(
                "'Buchen' sichert Ihre (überarbeiteten) Produkte aus der Übersicht "
                "in der 'Bestellungen' Tabelle. Zudem werden die Lieferdaten "
                "für die nächsten Bestellungen berechnet (basierend auf den Abos "
                "in der Datenbank!). ACHTUNG: Sobald Sie die Übersicht buchen, können "
                "Sie keine Änderungen mehr an den morgigen Lieferungen durchführen!!!"
                ),
            'delivery_download_tooltip':(
                "Download der aktuellen Übersicht als Excel."
                ),

            'delivery_category_table_name':"Produkt Übersicht",
            'delivery_orders_table_name':"Bestellungen",

            'delivery_product_overview':"Produkte",
            'delivery_product_overview_description':(
                "Eine Übersicht über die Anzahl an benötigten Produkten "
                "für die nächste Lieferung."
                ),

            'delivery_category_overview':"Kategorien",
            'delivery_category_overview_description':(
                "Übersicht der benötigten Produkte nach Kategorien."
                ),
            'delivery_category_table_section_name':"Alle",
            
            'delivery_total_earnings':"Einnahmen",
            'delivery_total_earnings_description':"Einnahmen nach morgiger Lieferung.",

            'delivery_total_spendings':"Ausgaben",
            'delivery_total_spendings_description':"Einkaufspreis für alle Produkte",
        },
        '/management':{
            'management_title':"Management",
            'management_lead':"Organisieren und bearbeiten Sie Ihre Daten.",
            'management_customers_btn':"Konsumenten",
            'management_category_btn':"Kategorien",
            'management_subcategory_btn':"Subkategorien",
            'management_products_btn':"Produkte",
            'management_bulk_btn':"Massen upload",
            'management_abo_btn':"Abos",
            'managment_abo_btn_label':"abo",
            'management_tbl_col_remover':"Löschen",
            'management_tbl_col_updater':"Update",
            'management_tbl_col_special':"Spezial",
            'management_auto_text':"Auto.",
            'management_no_data':"Keine Daten verfügbar!",
        },
        '/bulk':{
            'bulk_title':"Massen Upload",
            'bulk_lead':(
                "Fügen Sie mehrer Datenbankeinträge durch Nutzung einer Excel "
                "Blaupause zu einer <span class='text-info'>"
                "Tablle</span> (e.g. Konsumente) hinzu."
            ),
            'bulk_select_blueprint':"1. Auswahl der zu erzeugenden Blaupause",
            'bulk_customers_btn':"Konsumenten",
            'bulk_category_btn':"Kategorien",
            'bulk_subcategory_btn':"Subkategorien",
            'bulk_products_btn':"Produkte",
            'bulk_abo_btn':"Abos",
            'bulk_edit_blueprints':"2. Blaupause bearbeiten",
            'bulk_edit_addition':(
                "Gehen Sie zu dem Ordner 'mini-moi/blueprints' in Ihrem Benutzerordner "
                "und kopieren Sie die gewünschten Datenbankeinträge in Ihre Excel Datei. <br>"
                "Achtung: Bitte NICHT die Spaltennamen ändern!"
            ),
            'bulk_push_the_button':"3. Den Knopf drücken",
            'bulk_push_it':(
                "Nachdem Sie Ihre Blaupause bearbeitet haben, müssen Sie nur noch den "
                "roten Knopf dürcken. <br>"
                "<span class='text-danger'>Achtung: Nachdem der Upload abgeschlossen ist "
                "wird die entsprechende Blaupause gelöscht. Sollten Sie diese weiterhin "
                "benötigen, so müssen Sie hiervon bitte eine Kopie anlegen! </span>"
            )
        },
        '/reporting':{
            'reporting_title':"Dashboard",
            'reporting_lead':"Übersicht über die letzten Einnahmen.",
            'reporting_current_week':"Übersicht zur aktuellen Woche",
            'reporting_last_week':"Übersicht zur letzten Woche",
            'reporting_month':"Übersicht zum aktuellen Monat",
            'reporting_year':"Übersicht zum aktuellen Jahr",
            'reporting_earning_spending':"Einnahmen",
            'reporting_revenue_source':"Einnahme Quellen",
            'reporting_selling_count':"Verkaufsübersicht",
            'reporting_no_data_available':"Keine Daten verfügbar!",
        },
        '/demo':{
            'demo_title':"Demo",
            'demo_lead':(
                "Lassen Sie die App mit Demo Daten laufen!"
            ),
            'demo_create_db':"Demo Daten erzeugen",
            'demo_warning':(
                "Sie können jederzeit Demo Daten zum testen dieser App "
                "erzeugen. <br>"
                "Sobald Sie auf den Knopf unten drücken, wird für <b>"
                "Mini Moi</b> eine neue Datenbank erstellt. Zu dieser "
                "werden anschließend Test-Daten hinzugefügt. <br> <br>"
                "<span class='text-danger'>ACHTUNG: <br>"
                "Aktuelle Daten in Ihrer Datenbank werden dadurch gelöscht! "
                "Sollten Sie bereits wichtige Daten eingepflegt haben, so sollten "
                "Sie zuvor ein Backup der Datenbank (im Einstellungsmenü) erstellen! "
                "</span>"
                ),
            'demo_btn':"Demo Daten erstellen!",
            'demo_creation_successfull':"Erledigt! Viel Spaß beim testen der App :-)",
        },
    },
    'notification':{
        'save_path':"Ihre Datei wurde gespeichert unter: {path}",
        'added_to_db':"'{element}' wurde erfolgreich hinzugefügt! Bitte aktualisieren Sie die Ansicht.",
        'deleted_from_db':"'{element}' erfolgreich gelöscht!",
        'update_to_db':"'{element}' erfolgreich geupdated!",
        'db_backup_success':"Backup erfolgreich erstellt. Gespeichert unter: {directory}",
        'db_rollback_success':"Datenbank wurde erfolgreich zu dem Stand von {file} wiederhergestellt.",
        'blueprint_created':"Die Blaupause für '{blueprint}' wurde erfolgreich unter '{path}' erstellt.",
        'bulkFinished':"Erfolgreich: {success}, Fehler: {failures}",
        'is_empty':"ist leer",
    },
    'column_mapping':{
        'customers':{
            'id':"id",
            'date':"Datum",
            'name':"Name",
            'surname':"Nachname",
            'street':"Straße",
            'nr':"Nr",
            'postal':"PLZ",
            'town':"Ort",
            'phone':"Tel.",
            'mobile':"Mobile",
            'birthdate':"Geburtstag",
            'approach':"Anfahrt",
            'notes':"Notiz"
            },
        'categories':{
            'id':"id",
            'name':"Name"
            },
        'products':{
            'id':"id",
            'name':"Name",
            'category':"Kategorie",
            'purchase_price':"Einkaufspreis",
            'selling_price':"Verkaufspreis",
            'margin':"Marge",
            'store':"Laden",
            'phone':"Tel.",
            },
        'abo':{
            'id':"id",
            'customer_id':"Konsumenten id",
            'update_date':"Update Tag",
            'cycle_type':"Zyklus",
            'interval':"Intervall",
            'next_delivery':"Nächste Lieferung",
            'product':"Produkt",
            'subcategory':"Subkategorie",
            'quantity':"Qnt."
        }
    },
    'table_mapping': {
        'customers':"Konsumenten",
        'customer':"Konsument",
        'categories':"Kategorien",
        'category':"Kategorie",
        'subcategories':"Subkategorien",
        'subcategory':"Subkategorie",
        'products':"Produkte",
        'product':"Produkt",
        'abos':"Abos",
        'abo':"Abo"
    },
    'cycle_type_mapping':{
        'None':"None",
        'day':"Wochentag",
        'interval':"Intervall"
    },
    'weekday_mapping':{
        0:"Montag",
        1:"Dienstag",
        2:"Mittwoch",
        3:"Donnerstag",
        4:"Freitag",
        5:"Samstag",
        6:"Sonntag",
    },
    'month_mapping':{
        1:"Januar",
        2:"Februar",
        3:"März",
        4:"April",
        5:"Mai",
        6:"Juni",
        7:"Juli",
        8:"August",
        9:"September",
        10:"Oktober",
        11:"November",
        12:"Dezember",
    },
    'formats':{
        'birthdate':"Jahr.Monat.Tag",
    },
    'type_mapping':{
        'str':"Text",
        'int':"Zahl (ganz)",
        'float':"Dezimalzahl"
    },
    'operation_mapping':{
        'add':"hinzufügen",
        'update':"aktualisieren",
        'delete':"löschen"
    }
    
}