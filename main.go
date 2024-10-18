package main

import (
	"fmt"
	"github.com/ayush-git-hub/CustomDB/Code/KVStoreImplement"
	"github.com/briandowns/spinner"
	"github.com/fatih/color"
	"github.com/common-nighthawk/go-figure"
	"strings"
	"time"
)

const PATH string = "./Sqlite.db"

var (
	// Enhanced color functions
	success = color.New(color.FgGreen, color.Bold).SprintFunc()
	failure = color.New(color.FgRed, color.Bold).SprintFunc()
	info    = color.New(color.FgCyan, color.Bold).SprintFunc()
	prompt  = color.New(color.FgYellow, color.Bold).SprintFunc()
	header  = color.New(color.FgMagenta, color.Bold).SprintFunc()
	highlight = color.New(color.FgHiWhite, color.Bold).SprintFunc()
	
	// Enhanced symbols
	tickMark  = success("✓")
	crossMark = failure("✗")
	star      = info("★")
	arrow     = prompt("➜")
	diamond   = header("◆")
)

func showSpinner(message string) *spinner.Spinner {
	s := spinner.New(spinner.CharSets[35], 80*time.Millisecond) // More dynamic spinner
	s.Suffix = " " + message
	s.Color("magenta", "bold")
	s.Start()
	return s
}

func showBanner() {
	// Create ASCII art banner
	myFigure := figure.NewFigure("CustomDB", "isometric1", true)
	bannerText := myFigure.String()
	
	decorativeLine := strings.Repeat(string(diamond), 50)
	
	fmt.Println(header(decorativeLine))
	fmt.Println(info(bannerText))
	fmt.Println(header(decorativeLine))
	
	subTitle := figure.NewFigure("In Golang", "small", true)
	fmt.Println(prompt(subTitle.String()))
}

func showMenu() {
	menu := `
╔════════════════ ` + highlight("Available Commands") + ` ═══════════════╗

  ` + star + `  ` + prompt("SET") + `  - Store a new key-value pair
  ` + star + `  ` + prompt("GET") + `  - Retrieve stored value by key
  ` + star + `  ` + prompt("DEL") + `  - Remove a key-value pair
  ` + star + `  ` + prompt("EXIT") + ` - Close the database

╚═══════════════════════════════════════════════╝

` + info("Tips:") + `
 ➤ Commands are case-insensitive
 ➤ Keys are unique identifiers
 ➤ Values can be any string
`
	fmt.Print(menu)
}

func showStatus(message string, isError bool) {
	timestamp := time.Now().Format("15:04:05")
	status := success("SUCCESS")
	if isError {
		status = failure("FAILED")
	}
	fmt.Printf("[%s] %s: %s\n", highlight(timestamp), status, message)
}

func main() {
	showBanner()
	
	s := showSpinner("Initializing CustomDB...")
	time.Sleep(1 * time.Second) // Add slight delay for visual effect
	
	db := KVStoreImplement.KV{Path: PATH}
	if err := db.Open(); err != nil {
		s.Stop()
		showStatus("Database initialization failed: "+err.Error(), true)
		return
	}
	s.Stop()
	showStatus("Database initialized successfully", false)
	
	defer db.Close()

	showMenu()

	for {
		fmt.Print(arrow + prompt(" Enter command: "))
		var op string
		fmt.Scanln(&op)
		op = strings.ToLower(strings.TrimSpace(op))

		switch op {
		case "set":
			set(&db)
		case "get":
			get(&db)
		case "del":
			del(&db)
		case "exit":
			s := showSpinner("Closing database...")
			time.Sleep(500 * time.Millisecond)
			s.Stop()
			showStatus("Database closed successfully", false)
			return
		default:
			fmt.Printf("%s %s\n", crossMark, failure("Invalid command. Please try again."))
			showMenu()
		}
	}
}

func set(db *KVStoreImplement.KV) {
	fmt.Print("\n" + diamond + prompt(" Enter key: "))
	var key string
	fmt.Scanln(&key)

	fmt.Print(diamond + prompt(" Enter value: "))
	var val string
	fmt.Scanln(&val)

	s := showSpinner("Setting key-value pair...")
	time.Sleep(500 * time.Millisecond) // Add slight delay for visual effect
	
	if err := db.Set([]byte(key), []byte(val)); err != nil {
		s.Stop()
		showStatus("Failed to set key-value pair: "+err.Error(), true)
		return
	}
	s.Stop()
	showStatus(fmt.Sprintf("Set key '%s' with value '%s'", highlight(key), highlight(val)), false)
}

func get(db *KVStoreImplement.KV) {
	fmt.Print("\n" + diamond + prompt(" Enter key: "))
	var key string
	fmt.Scanln(&key)

	s := showSpinner("Retrieving value...")
	time.Sleep(500 * time.Millisecond) // Add slight delay for visual effect
	
	val, found := db.Get([]byte(key))
	s.Stop()

	if !found {
		showStatus(fmt.Sprintf("Key '%s' not found", highlight(key)), true)
	} else {
		showStatus(fmt.Sprintf("Found value for key '%s': %s", highlight(key), highlight(string(val))), false)
	}
}

func del(db *KVStoreImplement.KV) {
	fmt.Print("\n" + diamond + prompt(" Enter key: "))
	var key string
	fmt.Scanln(&key)

	s := showSpinner("Deleting key...")
	time.Sleep(500 * time.Millisecond) // Add slight delay for visual effect
	
	deleted, err := db.Del([]byte(key))
	s.Stop()

	if err != nil {
		showStatus("Failed to delete key: "+err.Error(), true)
		return
	}

	if deleted {
		showStatus(fmt.Sprintf("Successfully deleted key '%s'", highlight(key)), false)
	} else {
		showStatus(fmt.Sprintf("Key '%s' not found", highlight(key)), true)
	}
}