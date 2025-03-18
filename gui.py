import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Import core functions from test.py
from banker_algorithm import read_input, calculate_need, is_safe, request_resources

FONT_SIZE = 13

class BankerAlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banker's Algorithm Visualization")
        self.root.geometry("1280x900")
        
        # Data structures to store system state
        self.n_processes = 0
        self.n_resources = 0
        self.available = []
        self.max_demand = []
        self.allocation = []
        self.need = []
        self.resource_names = ['A', 'B', 'C']  # Default resource names
        self.execution_steps = []
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create file input section
        self.file_frame = ttk.Frame(self.main_frame, padding="5")
        self.file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.file_frame, text="Input File:", font=("Arial",FONT_SIZE)).pack(side=tk.LEFT)
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.file_path, width=50, font=("Arial",FONT_SIZE))
        self.file_entry.pack(side=tk.LEFT, padx=5)
        
        self.browse_button = ttk.Button(self.file_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT)
        
        self.load_button = ttk.Button(self.file_frame, text="Load Data", command=self.load_data)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        # Create tab control for different views
        self.tab_control = ttk.Notebook(self.main_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tabs
        self.combined_tab = ttk.Frame(self.tab_control)
        self.request_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.combined_tab, text="System State & Execution Steps")
        self.tab_control.add(self.request_tab, text="Request Resources")
        
        # Setup combined tab
        self.setup_combined_tab()
        
        # Setup request tab
        self.setup_request_tab()
        
        # Safety status frame
        self.safety_frame = ttk.LabelFrame(self.main_frame, text="System Safety Status", padding="10")
        self.safety_frame.pack(fill=tk.X, pady=5, before=self.tab_control)
        
        self.safety_var = tk.StringVar()
        self.safety_label = ttk.Label(self.safety_frame, textvariable=self.safety_var, font=("Arial",FONT_SIZE, "bold"))
        self.safety_label.pack(fill=tk.X, expand=True)
        
        # Status bar
        self.status_frame = ttk.Frame(self.main_frame, padding="5")
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, font=("Arial",FONT_SIZE))
        self.status_label.pack(side=tk.LEFT)
        
    def setup_combined_tab(self):
        # # Create a paned window to allow resizing between matrices and steps
        # self.paned_window = ttk.PanedWindow(self.combined_tab, orient=tk.VERTICAL)
        # self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Create a paned window with horizontal orientation
        self.paned_window = ttk.PanedWindow(self.combined_tab, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Create matrices frame (left side - 5/7 of screen)
        self.matrices_frame = ttk.LabelFrame(self.paned_window, text="System Matrices", padding="10")
            
        # Create execution steps frame (right side - 2/7 of screen)
        self.steps_frame = ttk.LabelFrame(self.paned_window, text="Execution Steps", padding="10")
        
        # Add frames to paned window
        self.paned_window.add(self.matrices_frame, weight=1)
        self.paned_window.add(self.steps_frame, weight=1)
    
    def setup_request_tab(self):
        request_frame = ttk.Frame(self.request_tab, padding="10")
        request_frame.pack(fill=tk.BOTH, expand=True)
        
        # Process selection
        ttk.Label(request_frame, text="Select Process:", font=("Arial",FONT_SIZE)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.process_var = tk.StringVar()
        self.process_combo = ttk.Combobox(request_frame, textvariable=self.process_var, state="disabled", font=("Arial",FONT_SIZE))
        self.process_combo.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Resource request inputs
        self.resource_frame = ttk.Frame(request_frame)
        self.resource_frame.grid(row=1, column=0, columnspan=1, sticky=tk.W, pady=10)
        
        # Request button
        self.request_button = ttk.Button(request_frame, text="Make Request", 
                                         command=self.make_request, state="disabled")
        self.request_button.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Result display
        self.result_var = tk.StringVar()
        ttk.Label(request_frame, textvariable=self.result_var, font=("Arial",FONT_SIZE)).grid(row=3, column=0, 
                                                                   columnspan=2, pady=10)
        
        # Create a paned window to divide matrices and request steps
        self.request_paned = ttk.PanedWindow(request_frame, orient=tk.HORIZONTAL)
        self.request_paned.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)
        request_frame.rowconfigure(4, weight=1)
        request_frame.columnconfigure(0, weight=1)
        
        # Create a frame to display the matrices in the request tab
        self.request_matrices_frame = ttk.Frame(self.request_paned)
        
        # Create a frame to display request steps
        self.request_steps_frame = ttk.LabelFrame(self.request_paned, text="Request Steps", padding="10")
        
        # Add frames to paned window
        self.request_paned.add(self.request_matrices_frame, weight=1)
        self.request_paned.add(self.request_steps_frame, weight=1)

    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select input file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
    
    def load_data(self):
        try:
            filename = self.file_path.get()
            if not filename:
                messagebox.showerror("Error", "Please select an input file")
                return
            
            self.n_processes, self.n_resources, self.available, self.max_demand, self.allocation = read_input(filename)
            self.need = calculate_need(self.max_demand, self.allocation)
            
            # Set resource names (up to self.n_resources)
            self.resource_names = []
            for i in range(self.n_resources):
                self.resource_names.append(chr(65 + i))  # A, B, C, D, ...
            
            # Check system safety
            safe, sequence, steps = is_safe(self.available, self.max_demand, self.allocation, 
                                    self.n_processes, self.n_resources)
            
            self.execution_steps = steps
            
            if safe:
                self.safety_var.set(f"✓ SYSTEM IS SAFE - Safe Sequence: {' → '.join('P'+str(i) for i in sequence)}")
                self.safety_label.configure(foreground="green")
            else:
                self.safety_var.set("❌ SYSTEM IS UNSAFE - No safe sequence exists!")
                self.safety_label.configure(foreground="red")
            
            # Update matrices display
            self.update_matrices_display()
            
            # Update execution steps display
            self.update_steps_display()
            
            # Update request tab
            self.update_request_tab()
            
            self.status_var.set(f"Loaded {self.n_processes} processes, {self.n_resources} resources")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def update_matrices_display(self, frame=None):
        if frame is None:
            frame = self.matrices_frame
        
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Create a frame with borders for the matrix table
        table_frame = ttk.Frame(frame, borderwidth=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Headers
        header_row = 0
        ttk.Label(table_frame, text="", font=("Arial",FONT_SIZE, "bold"), 
                 borderwidth=1, relief="solid", padding=3).grid(row=header_row, column=0, sticky="nsew")
        
        # Allocation header
        ttk.Label(table_frame, text="Allocation", font=("Arial",FONT_SIZE, "bold"), 
                 borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
            row=header_row, column=1, columnspan=self.n_resources, sticky="nsew")
        
        # Max header
        ttk.Label(table_frame, text="Max", font=("Arial",FONT_SIZE, "bold"), 
                 borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
            row=header_row, column=1+self.n_resources, columnspan=self.n_resources, sticky="nsew")
        
        # Available header
        ttk.Label(table_frame, text="Available", font=("Arial",FONT_SIZE, "bold"), 
                 borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
            row=header_row, column=1+2*self.n_resources, columnspan=self.n_resources, sticky="nsew")
        
        # Need header
        ttk.Label(table_frame, text="Need = Max - Allocation", font=("Arial",FONT_SIZE, "bold"), 
                 borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
            row=header_row, column=1+3*self.n_resources, columnspan=self.n_resources, sticky="nsew")
        
        # Resource column headers (A B C etc.)
        resource_row = header_row + 1
        ttk.Label(table_frame, text="", font=("Arial",FONT_SIZE, "bold"), 
                 borderwidth=1, relief="solid", padding=3).grid(row=resource_row, column=0, sticky="nsew")
        
        # Allocation resource names
        for j in range(self.n_resources):
            ttk.Label(table_frame, text=self.resource_names[j], font=("Arial",FONT_SIZE, "bold"), 
                     borderwidth=1, relief="solid", padding=3, background="#f0f0f0").grid(
                row=resource_row, column=j+1, sticky="nsew")
        
        # Max resource names
        for j in range(self.n_resources):
            ttk.Label(table_frame, text=self.resource_names[j], font=("Arial",FONT_SIZE, "bold"), 
                     borderwidth=1, relief="solid", padding=3, background="#f0f0f0").grid(
                row=resource_row, column=j+1+self.n_resources, sticky="nsew")
        
        # Available resource names
        for j in range(self.n_resources):
            ttk.Label(table_frame, text=self.resource_names[j], font=("Arial",FONT_SIZE, "bold"), 
                     borderwidth=1, relief="solid", padding=3, background="#f0f0f0").grid(
                row=resource_row, column=j+1+2*self.n_resources, sticky="nsew")
        
        # Need resource names
        for j in range(self.n_resources):
            ttk.Label(table_frame, text=self.resource_names[j], font=("Arial",FONT_SIZE, "bold"), 
                     borderwidth=1, relief="solid", padding=3, background="#f0f0f0").grid(
                row=resource_row, column=j+1+3*self.n_resources, sticky="nsew")
        
        # Display available resources (just the row of values)
        avail_row = resource_row + 1
        ttk.Label(table_frame, text="", font=("Arial",FONT_SIZE), 
                 borderwidth=1, relief="solid", padding=3).grid(row=avail_row, column=0, sticky="nsew")
                
        # Empty cells for allocation and max columns in available row
        for j in range(self.n_resources * 2):
            ttk.Label(table_frame, text="", font=("Arial",FONT_SIZE), 
                     borderwidth=1, relief="solid", padding=3).grid(
                row=avail_row, column=j+1, sticky="nsew")
        
        # Available resources values
        for j in range(self.n_resources):
            ttk.Label(table_frame, text=str(self.available[j]), font=("Arial",FONT_SIZE), 
                     borderwidth=1, relief="solid", padding=3).grid(
                row=avail_row, column=j+1+2*self.n_resources, sticky="nsew")
        
        # Empty cells for need column in available row
        for j in range(self.n_resources):
            ttk.Label(table_frame, text="", font=("Arial",FONT_SIZE), 
                     borderwidth=1, relief="solid", padding=3).grid(
                row=avail_row, column=j+1+3*self.n_resources, sticky="nsew")
        
        # Display process data
        start_row = avail_row + 1
        for i in range(self.n_processes):
            # Process label
            ttk.Label(table_frame, text=f"P{i}", font=("Arial",FONT_SIZE, "bold"), 
                     borderwidth=1, relief="solid", padding=3, background="#f0f0f0").grid(
                row=start_row + i, column=0, sticky="nsew")
            
            # Allocation values
            for j in range(self.n_resources):
                ttk.Label(table_frame, text=str(self.allocation[i][j]), font=("Arial",FONT_SIZE), 
                         borderwidth=1, relief="solid", padding=3).grid(
                    row=start_row + i, column=j+1, sticky="nsew")
            
            # Max values
            for j in range(self.n_resources):
                ttk.Label(table_frame, text=str(self.max_demand[i][j]), font=("Arial",FONT_SIZE), 
                         borderwidth=1, relief="solid", padding=3).grid(
                    row=start_row + i, column=j+1+self.n_resources, sticky="nsew")
            
            # Empty cells in Available column for process rows
            for j in range(self.n_resources):
                ttk.Label(table_frame, text="", font=("Arial",FONT_SIZE), 
                         borderwidth=1, relief="solid", padding=3).grid(
                    row=start_row + i, column=j+1+2*self.n_resources, sticky="nsew")
            
            # Need values
            for j in range(self.n_resources):
                ttk.Label(table_frame, text=str(self.need[i][j]), font=("Arial",FONT_SIZE), 
                         borderwidth=1, relief="solid", padding=3).grid(
                    row=start_row + i, column=j+1+3*self.n_resources, sticky="nsew")
        
        # Apply some styling
        for widget in table_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(anchor="center", width=5)
    
    def update_steps_display(self):
        # Clear existing widgets
        for widget in self.steps_frame.winfo_children():
            widget.destroy()
            
        if not self.execution_steps:
            ttk.Label(self.steps_frame, text="No execution steps available or system is unsafe", 
                     font=("Arial",FONT_SIZE)).pack(pady=20)
            return
            
        # Create a scrollable frame for the execution steps
        outer_frame = ttk.Frame(self.steps_frame)
        outer_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a canvas with scrollbar
        canvas = tk.Canvas(outer_frame)
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Headers for each step
        current_row = 0
        for step_idx, step in enumerate(self.execution_steps):
            process_idx = step['process']
            
            # Frame for this step with borders
            step_frame = ttk.LabelFrame(scrollable_frame, text=f"Step {step_idx+1}: Execute P{process_idx}", 
                                      padding="10", borderwidth=2, relief="solid")
            step_frame.grid(row=current_row, column=0, sticky="ew", pady=5, padx=5)
            current_row += 1
            
            # Create table for step data
            step_table = ttk.Frame(step_frame)
            step_table.pack(fill=tk.BOTH, expand=True)
            
            # Work before execution
            ttk.Label(step_table, text="Available before:", font=("Arial",FONT_SIZE, "bold"),
                     borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
                row=0, column=0, sticky="nsew")
            
            # Create a bordered frame for resources
            before_frame = ttk.Frame(step_table)
            before_frame.grid(row=0, column=1, sticky="ew")
            
            for j in range(self.n_resources):
                ttk.Label(before_frame, text=f"{self.resource_names[j]}: {step['work_before'][j]}", 
                         font=("Arial",FONT_SIZE), borderwidth=1, relief="solid", padding=3).grid(
                    row=0, column=j, sticky="nsew")
            
            # Resources released
            ttk.Label(step_table, text="Resources released:", font=("Arial",FONT_SIZE, "bold"),
                     borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
                row=1, column=0, sticky="nsew")
            
            # Create a bordered frame for allocation
            alloc_frame = ttk.Frame(step_table)
            alloc_frame.grid(row=1, column=1, sticky="ew")
            
            for j in range(self.n_resources):
                ttk.Label(alloc_frame, text=f"{self.resource_names[j]}: {step['allocation'][j]}", 
                         font=("Arial",FONT_SIZE), borderwidth=1, relief="solid", padding=3).grid(
                    row=0, column=j, sticky="nsew")
            
            # Work after execution
            ttk.Label(step_table, text="Available after:", font=("Arial",FONT_SIZE, "bold"),
                     borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
                row=2, column=0, sticky="nsew")
            
            # Create a bordered frame for after resources
            after_frame = ttk.Frame(step_table)
            after_frame.grid(row=2, column=1, sticky="ew")
            
            for j in range(self.n_resources):
                ttk.Label(after_frame, text=f"{self.resource_names[j]}: {step['work_after'][j]}", 
                         font=("Arial",FONT_SIZE), borderwidth=1, relief="solid", padding=3).grid(
                    row=0, column=j, sticky="nsew")
    
    def update_request_tab(self):
        # Clear existing resource inputs
        for widget in self.resource_frame.winfo_children():
            widget.destroy()
        
        # Update process selection
        self.process_combo['values'] = [f'P{i}' for i in range(self.n_processes)]
        self.process_combo['state'] = 'readonly'
        self.process_combo.current(0)
        
        # Create resource inputs
        self.resource_entries = []
        for j in range(self.n_resources):
            ttk.Label(self.resource_frame, text=f"{self.resource_names[j]}:", font=("Arial",FONT_SIZE),
                     borderwidth=1, relief="solid", padding=3).grid(row=0, column=j*2, padx=2, pady=2)
            entry = ttk.Entry(self.resource_frame, width=5, font=("Arial",FONT_SIZE))
            entry.grid(row=0, column=j*2+1, padx=2, pady=2)
            entry.insert(0, "0")
            self.resource_entries.append(entry)
        
        # Enable request button
        self.request_button['state'] = 'normal'
        
        # Update matrices display in the request tab
        self.update_matrices_display(self.request_matrices_frame)
        
        # Initialize request steps display
        self.update_request_steps(None)
    
    def update_request_steps(self, steps):
        # Clear existing widgets
        for widget in self.request_steps_frame.winfo_children():
            widget.destroy()
            
        if not steps:
            ttk.Label(self.request_steps_frame, text="No execution steps available", 
                     font=("Arial",FONT_SIZE)).pack(pady=20)
            return
            
        # Create a scrollable frame for the execution steps
        outer_frame = ttk.Frame(self.request_steps_frame)
        outer_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a canvas with scrollbar
        canvas = tk.Canvas(outer_frame)
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Headers for each step
        current_row = 0
        for step_idx, step in enumerate(steps):
            process_idx = step['process']
            
            # Frame for this step with borders
            step_frame = ttk.LabelFrame(scrollable_frame, text=f"Step {step_idx+1}: Execute P{process_idx}", 
                                      padding="10", borderwidth=2, relief="solid")
            step_frame.grid(row=current_row, column=0, sticky="ew", pady=5, padx=5)
            current_row += 1
            
            # Create table for step data
            step_table = ttk.Frame(step_frame)
            step_table.pack(fill=tk.BOTH, expand=True)
            
            # Work before execution
            ttk.Label(step_table, text="Available before:", font=("Arial",FONT_SIZE, "bold"),
                     borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
                row=0, column=0, sticky="nsew")
            
            # Create a bordered frame for resources
            before_frame = ttk.Frame(step_table)
            before_frame.grid(row=0, column=1, sticky="ew")
            
            for j in range(self.n_resources):
                ttk.Label(before_frame, text=f"{self.resource_names[j]}: {step['work_before'][j]}", 
                         font=("Arial",FONT_SIZE), borderwidth=1, relief="solid", padding=3).grid(
                    row=0, column=j, sticky="nsew")
            
            # Resources released
            ttk.Label(step_table, text="Resources released:", font=("Arial",FONT_SIZE, "bold"),
                     borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
                row=1, column=0, sticky="nsew")
            
            # Create a bordered frame for allocation
            alloc_frame = ttk.Frame(step_table)
            alloc_frame.grid(row=1, column=1, sticky="ew")
            
            for j in range(self.n_resources):
                ttk.Label(alloc_frame, text=f"{self.resource_names[j]}: {step['allocation'][j]}", 
                         font=("Arial",FONT_SIZE), borderwidth=1, relief="solid", padding=3).grid(
                    row=0, column=j, sticky="nsew")
            
            # Work after execution
            ttk.Label(step_table, text="Available after:", font=("Arial",FONT_SIZE, "bold"),
                     borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
                row=2, column=0, sticky="nsew")
            
            # Create a bordered frame for after resources
            after_frame = ttk.Frame(step_table)
            after_frame.grid(row=2, column=1, sticky="ew")
            
            for j in range(self.n_resources):
                ttk.Label(after_frame, text=f"{self.resource_names[j]}: {step['work_after'][j]}", 
                         font=("Arial",FONT_SIZE), borderwidth=1, relief="solid", padding=3).grid(
                    row=0, column=j, sticky="nsew")
    
    def make_request(self):
        try:
            process_idx = int(self.process_var.get()[1:])  # Extract number from 'P0', 'P1', etc.
            
            # Get request values
            request = []
            for entry in self.resource_entries:
                value = entry.get().strip()
                if not value:
                    messagebox.showerror("Error", "Please enter all resource values")
                    return
                request.append(int(value))
            
            if len(request) != self.n_resources:
                messagebox.showerror("Error", f"Must specify {self.n_resources} resource values")
                return
            
            # Process the request
            success, result, steps = request_resources(
                process_idx, request, self.available, 
                self.max_demand, self.allocation, self.n_resources
            )
            
            if success:
                # Update system state
                for j in range(self.n_resources):
                    self.available[j] -= request[j]
                    self.allocation[process_idx][j] += request[j]
                self.need = calculate_need(self.max_demand, self.allocation)
                
                # Update execution steps
                self.execution_steps = steps
                self.result_var.set(f"Request granted! System is safe.\nSafe sequence: {' → '.join('P'+str(i) for i in result)}")
                
                # Update displays
                self.update_matrices_display()
                self.update_matrices_display(self.request_matrices_frame)
                self.update_steps_display()
                self.update_request_steps(steps)
            else:
                self.result_var.set(result)
                # If request would make system unsafe
                # Create temporary copies to show what would happen
                temp_available = self.available.copy()
                temp_allocation = [row.copy() for row in self.allocation]
                temp_need = [row.copy() for row in self.need]

                # Apply the request to the temporary copies
                for j in range(self.n_resources):
                    temp_available[j] -= request[j]
                    temp_allocation[process_idx][j] += request[j]
                    temp_need[process_idx][j] -= request[j]

                # Save original values
                original_available = self.available
                original_allocation = self.allocation
                original_need = self.need

                # Temporarily set system state to show what would happen
                self.available = temp_available
                self.allocation = temp_allocation
                self.need = temp_need

                # Update only the request tab matrices to show unsafe state
                self.update_matrices_display(self.request_matrices_frame)

                # Update steps display (will show "No execution steps available")
                self.update_request_steps(None)

                # Add additional message explaining why
                ttk.Label(self.request_steps_frame, text="System would be unsafe - no safe execution sequence possible", 
                         font=("Arial",FONT_SIZE), foreground="red").pack(pady=10)

                # Restore original system state
                self.available = original_available
                self.allocation = original_allocation
                self.need = original_need
        
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

class DeadlockDetectionAlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Detection Algorithm")
        self.root.geometry("1280x850")
        
        # Data structures to store system state
        self.n_processes = 0
        self.n_resources = 0
        self.available = []
        self.allocation = []
        self.request = []
        self.resource_names = ['A', 'B', 'C']  # Default resource names
        self.execution_sequence = []
        self.deadlocked_processes = []
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create file input section
        self.file_frame = ttk.Frame(self.main_frame, padding="5")
        self.file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.file_frame, text="Input File:", font=("Arial", FONT_SIZE)).pack(side=tk.LEFT)
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.file_path, width=50, font=("Arial", FONT_SIZE))
        self.file_entry.pack(side=tk.LEFT, padx=5)
        
        self.browse_button = ttk.Button(self.file_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT)
        
        self.load_button = ttk.Button(self.file_frame, text="Load Data", command=self.load_data)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.detect_button = ttk.Button(self.file_frame, text="Detect Deadlock", command=self.detect_deadlock, state="disabled")
        self.detect_button.pack(side=tk.LEFT, padx=5)
        
        # Create main content area with tables and results
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create matrices display frame
        self.matrices_frame = ttk.LabelFrame(self.content_frame, text="System Matrices", padding="10")
        self.matrices_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        
        # Create new request frame
        self.new_request_frame = ttk.LabelFrame(self.content_frame, text="Add New Request", padding="10")
        self.new_request_frame.pack(fill=tk.X, expand=False, side=tk.TOP, pady=10)
        
        # Setup new request UI components
        self.setup_new_request_ui()
        
        # Create results frame
        self.results_frame = ttk.LabelFrame(self.content_frame, text="Detection Results", padding="10")
        self.results_frame.pack(fill=tk.X, expand=False, side=tk.BOTTOM, pady=10)
        
        # Status display
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self.results_frame, textvariable=self.status_var, 
                                     font=("Arial", FONT_SIZE, "bold"))
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Sequence or deadlock display
        self.result_text = tk.Text(self.results_frame, height=6, font=("Arial", FONT_SIZE))
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def setup_new_request_ui(self):
        request_frame = ttk.Frame(self.new_request_frame)
        request_frame.pack(fill=tk.X, expand=True, pady=5)
        
        # Process selection
        ttk.Label(request_frame, text="Process:", font=("Arial", FONT_SIZE)).pack(side=tk.LEFT, padx=5)
        self.process_var = tk.StringVar()
        self.process_combo = ttk.Combobox(request_frame, textvariable=self.process_var, state="disabled", 
                                         font=("Arial", FONT_SIZE), width=5)
        self.process_combo.pack(side=tk.LEFT, padx=5)
        
        # Resource entries frame
        self.resource_entries_frame = ttk.Frame(request_frame)
        self.resource_entries_frame.pack(side=tk.LEFT, padx=5)
        
        # Add request button
        self.add_request_button = ttk.Button(request_frame, text="Add Request", 
                                           command=self.add_new_request, state="disabled")
        self.add_request_button.pack(side=tk.LEFT, padx=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select input file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)

    def load_data(self):
        try:
            filename = self.file_path.get()
            if not filename:
                messagebox.showerror("Error", "Please select an input file")
                return
            
            # Read the deadlock detection input file
            # Format: [n_processes] [n_resources]
            #         [available resources]
            #         [allocation matrix]
            #         [request matrix]
            with open(filename, 'r') as file:
                line = file.readline().strip().split()
                self.n_processes = int(line[0])
                self.n_resources = int(line[1])
                
                # Read available resources
                line = file.readline().strip().split()
                self.available = [int(x) for x in line]
                
                # Read allocation matrix
                self.allocation = []
                for _ in range(self.n_processes):
                    line = file.readline().strip().split()
                    self.allocation.append([int(x) for x in line])
                
                # Read request matrix
                self.request = []
                for _ in range(self.n_processes):
                    line = file.readline().strip().split()
                    self.request.append([int(x) for x in line])
            
            # Set resource names (up to self.n_resources)
            self.resource_names = []
            for i in range(self.n_resources):
                self.resource_names.append(chr(65 + i))  # A, B, C, D, ...
            
            # Update matrices display
            self.update_matrices_display()
            
            # Enable detect button and request UI
            self.detect_button['state'] = 'normal'
            self.process_combo['values'] = [f'P{i}' for i in range(self.n_processes)]
            self.process_combo['state'] = 'readonly'
            if self.n_processes > 0:
                self.process_combo.current(0)
            self.add_request_button['state'] = 'normal'
            
            # Setup resource entry fields
            self.setup_resource_entries()
            
            self.status_var.set(f"Data loaded: {self.n_processes} processes, {self.n_resources} resources")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def setup_resource_entries(self):
        # Clear existing entries
        for widget in self.resource_entries_frame.winfo_children():
            widget.destroy()
        
        # Create new entry fields for each resource
        self.resource_entries = []
        for i in range(self.n_resources):
            resource_frame = ttk.Frame(self.resource_entries_frame)
            resource_frame.pack(side=tk.LEFT, padx=2)
            
            ttk.Label(resource_frame, text=f"{self.resource_names[i]}:", 
                    font=("Arial", FONT_SIZE)).pack(side=tk.LEFT)
            entry = ttk.Entry(resource_frame, width=3, font=("Arial", FONT_SIZE))
            entry.pack(side=tk.LEFT)
            entry.insert(0, "0")
            self.resource_entries.append(entry)

    def update_matrices_display(self):
        # Clear existing widgets
        for widget in self.matrices_frame.winfo_children():
            widget.destroy()
        
        # Create a frame with borders for the matrix table
        table_frame = ttk.Frame(self.matrices_frame, borderwidth=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Headers
        ttk.Label(table_frame, text="", font=("Arial", FONT_SIZE, "bold"), 
                 borderwidth=1, relief="solid", padding=3).grid(row=0, column=0, sticky="nsew")
        
        # Allocation header
        ttk.Label(table_frame, text="Allocation", font=("Arial", FONT_SIZE, "bold"), 
                 borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
            row=0, column=1, columnspan=self.n_resources, sticky="nsew")
        
        # Request header
        ttk.Label(table_frame, text="Request", font=("Arial", FONT_SIZE, "bold"), 
                 borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
            row=0, column=1+self.n_resources, columnspan=self.n_resources, sticky="nsew")
        
        # Available header
        ttk.Label(table_frame, text="Available", font=("Arial", FONT_SIZE, "bold"), 
                 borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
            row=0, column=1+2*self.n_resources, columnspan=self.n_resources, sticky="nsew")
        
        # # Request <= Available header
        # ttk.Label(table_frame, text="Request <= Available", font=("Arial", FONT_SIZE, "bold"), 
        #          borderwidth=1, relief="solid", padding=3, background="#e0e0e0").grid(
        #     row=0, column=1+3*self.n_resources, sticky="nsew")
        
        # Resource column headers (A B C etc.)
        for j in range(self.n_resources):
            ttk.Label(table_frame, text=self.resource_names[j], font=("Arial", FONT_SIZE, "bold"), 
                     borderwidth=1, relief="solid", padding=3, background="#f0f0f0").grid(
                row=1, column=j+1, sticky="nsew")
            
            ttk.Label(table_frame, text=self.resource_names[j], font=("Arial", FONT_SIZE, "bold"), 
                     borderwidth=1, relief="solid", padding=3, background="#f0f0f0").grid(
                row=1, column=j+1+self.n_resources, sticky="nsew")
            
            ttk.Label(table_frame, text=self.resource_names[j], font=("Arial", FONT_SIZE, "bold"), 
                     borderwidth=1, relief="solid", padding=3, background="#f0f0f0").grid(
                row=1, column=j+1+2*self.n_resources, sticky="nsew")
        
        # Display available resources
        ttk.Label(table_frame, text="", font=("Arial", FONT_SIZE), 
                 borderwidth=1, relief="solid", padding=3).grid(row=2, column=0, sticky="nsew")
                
        # Empty cells for allocation and request columns in available row
        for j in range(self.n_resources * 2):
            ttk.Label(table_frame, text="", font=("Arial", FONT_SIZE), 
                     borderwidth=1, relief="solid", padding=3).grid(
                row=2, column=j+1, sticky="nsew")
        
        # Available resources values
        for j in range(self.n_resources):
            ttk.Label(table_frame, text=str(self.available[j]), font=("Arial", FONT_SIZE), 
                     borderwidth=1, relief="solid", padding=3).grid(
                row=2, column=j+1+2*self.n_resources, sticky="nsew")
        
        # Empty cell for Request <= Available in available row
        ttk.Label(table_frame, text="", font=("Arial", FONT_SIZE), 
                 borderwidth=1, relief="solid", padding=3).grid(
            row=2, column=1+3*self.n_resources, sticky="nsew")
        
        # Display process data
        for i in range(self.n_processes):
            # Process label
            ttk.Label(table_frame, text=f"P{i}", font=("Arial", FONT_SIZE, "bold"), 
                     borderwidth=1, relief="solid", padding=3, background="#f0f0f0").grid(
                row=i+3, column=0, sticky="nsew")
            
            # Allocation values
            for j in range(self.n_resources):
                ttk.Label(table_frame, text=str(self.allocation[i][j]), font=("Arial", FONT_SIZE), 
                         borderwidth=1, relief="solid", padding=3).grid(
                    row=i+3, column=j+1, sticky="nsew")
            
            # Request values
            for j in range(self.n_resources):
                ttk.Label(table_frame, text=str(self.request[i][j]), font=("Arial", FONT_SIZE), 
                         borderwidth=1, relief="solid", padding=3).grid(
                    row=i+3, column=j+1+self.n_resources, sticky="nsew")
            
            # Empty cells in Available column for process rows
            for j in range(self.n_resources):
                ttk.Label(table_frame, text="", font=("Arial", FONT_SIZE), 
                         borderwidth=1, relief="solid", padding=3).grid(
                    row=i+3, column=j+1+2*self.n_resources, sticky="nsew")
            
            # Check if request <= for this process
            request_le_available = True
            for j in range(self.n_resources):
                if self.request[i][j] > self.available[j]:
                    request_le_available = False
                    break
            
            # # Display whether request <= available
            # bg_color = "#d4f7d4" if request_le_available else "#ffcccc"
            # text = "Yes" if request_le_available else "No"
            # ttk.Label(table_frame, text=text, font=("Arial", FONT_SIZE), 
            #          borderwidth=1, relief="solid", padding=3, background=bg_color).grid(
            #     row=i+3, column=1+3*self.n_resources, sticky="nsew")
        
        # Apply some styling
        for widget in table_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(anchor="center", width=5)

    def add_new_request(self):
        try:
            if not self.process_var.get():
                messagebox.showerror("Error", "Please select a process")
                return
                
            process_idx = int(self.process_var.get()[1:])  # Extract number from 'P0', 'P1', etc.
            
            # Get request values
            new_request = []
            for entry in self.resource_entries:
                value = entry.get().strip()
                if not value:
                    messagebox.showerror("Error", "Please enter all resource values")
                    return
                new_request.append(int(value))
            
            # Update request matrix
            for j in range(self.n_resources):
                self.request[process_idx][j] = new_request[j]
            
            # Update display
            self.update_matrices_display()
            self.status_var.set(f"Added new request for P{process_idx}: {new_request}")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def detect_deadlock(self):
        # Implement deadlock detection algorithm
        work = self.available.copy()
        finish = [False] * self.n_processes
        execution_sequence = []

        # Mark processes with no resources allocated as already finished
        for i in range(self.n_processes):
            if all(self.allocation[i][j] == 0 for j in range(self.n_resources)):
                finish[i] = True
                execution_sequence.append(i)  # Add to execution sequence since it's already done
        
        # Keep trying to find unfinished processes that can complete
        change = True
        while change:
            change = False
            for i in range(self.n_processes):
                if not finish[i]:
                    # Check if request can be satisfied with available resources
                    can_finish = True
                    for j in range(self.n_resources):
                        if self.request[i][j] > work[j]:
                            can_finish = False
                            break
                    
                    if can_finish:
                        # Process can finish, update work and mark as finished
                        for j in range(self.n_resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        execution_sequence.append(i)
                        change = True
        
        # Check for deadlock
        self.deadlocked_processes = []
        for i in range(self.n_processes):
            if not finish[i]:
                self.deadlocked_processes.append(i)
        
        self.execution_sequence = execution_sequence
        self.display_results(finish)

    def display_results(self, finish):
        self.result_text.delete(1.0, tk.END)
        
        if all(finish):
            # No deadlock
            self.status_var.set("✓ NO DEADLOCK DETECTED")
            self.status_label.configure(foreground="green")
            
            sequence_str = " → ".join(f"P{i}" for i in self.execution_sequence)
            self.result_text.insert(tk.END, f"System is not deadlocked\n")
            self.result_text.insert(tk.END, f"Safe execution sequence: {sequence_str}\n")
        else:
            # Deadlock detected
            self.status_var.set("❌ DEADLOCK DETECTED")
            self.status_label.configure(foreground="red")
            
            deadlocked_str = ", ".join(f"P{i}" for i in self.deadlocked_processes)
            self.result_text.insert(tk.END, f"System is deadlocked\n")
            self.result_text.insert(tk.END, f"Deadlocked processes: {deadlocked_str}\n\n")
            
            # Show process status with detailed request information for deadlocked processes
            self.result_text.insert(tk.END, "Process Status:\n")
            for i in range(self.n_processes):
                status = "Not Deadlocked" if finish[i] else "DEADLOCKED"
                color = "green" if finish[i] else "red"
                
                self.result_text.insert(tk.END, f"P{i}: {status}", (f"color_{i}",))
                self.result_text.tag_configure(f"color_{i}", foreground=color)
                
                # For deadlocked processes, show their request
                if not finish[i]:
                    request_str = ", ".join(f"{self.resource_names[j]}:{self.request[i][j]}" 
                                          for j in range(self.n_resources))
                    self.result_text.insert(tk.END, f" - Request: [{request_str}]")
                
                self.result_text.insert(tk.END, "\n")
            
            # Show why deadlock occurred - explain requests that can't be satisfied
            self.result_text.insert(tk.END, "\nReason for deadlock:\n")
            for i in self.deadlocked_processes:
                unsatisfied = []
                for j in range(self.n_resources):
                    if self.request[i][j] > self.available[j]:
                        unsatisfied.append(f"{self.resource_names[j]}(needs {self.request[i][j]}, available {self.available[j]})")
                
                if unsatisfied:
                    self.result_text.insert(tk.END, f"P{i} - Request exceeds available resources: {', '.join(unsatisfied)}\n")
                