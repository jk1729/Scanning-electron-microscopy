import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os
from pathlib import Path

class SEMSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("SEM Simulator - Virtual Scanning Electron Microscope")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f0f0")
        
        # State management
        self.chamber_evacuated = False
        self.hv_on = False
        self.current_sample = None
        self.current_image = None
        self.current_image_pil = None
        
        # Sample database
        self.samples = {
            "Arthropods": ["Ant eye", "Spider silk"],
            "Everyday Things": ["Sugar crystals", "Table salt", "Kitchen sponge"],
            "Forensic material": ["Human hair", "Polyester fiber", "Paper fiber"],
            "Hydrophobic surfaces": ["Butterfly wing", "Gecko skin", "Lotus leaf"]
        }
        
        self.sample_images = {
            "Ant eye": "samples/ant-eye.jpg",
            "Spider silk": "samples/spider-silk.jpg",
            "Sugar crystals": "samples/sugar-crystals.jpg",
            "Table salt": "samples/table-salt.jpg",
            "Kitchen sponge": "samples/kitchen-sponge.jpg",
            "Human hair": "samples/human-hair.jpg",
            "Polyester fiber": "samples/polyester-fiber.jpg",
            "Paper fiber": "samples/paper-fiber.jpg",
            "Butterfly wing": "samples/butterfly-wing.jpg",
            "Gecko skin": "samples/gecko-skin.jpg",
            "Lotus leaf": "samples/lotus-leaf.jpg",
        }
        
        self.voltage_options = [5, 10, 15, 20, 30]  # kV
        self.spot_size_options = [5, 10, 15, 20]     # nm
        self.height_options = [8, 10, 20]            # mm
        
        # Create UI
        self.create_header()
        self.create_main_layout()
        self.update_status()
        
    def create_header(self):
        """Create header section"""
        header = tk.Frame(self.root, bg="#1e3a5f", height=80)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="SEM SIMULATOR", font=("Arial", 32, "bold"), 
                        fg="#5fa3d0", bg="#1e3a5f")
        title.pack(pady=10)
        
        subtitle = tk.Label(header, text="A simplified, interactive simulation.", 
                           font=("Arial", 12), fg="#9db4c8", bg="#1e3a5f")
        subtitle.pack()
    
    def create_main_layout(self):
        """Create main layout with scrollable left panel, center canvas, right info"""
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel frame with scrollbar
        left_panel_outer = tk.Frame(main_frame, bg="#b0b0b0", width=320)
        left_panel_outer.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Canvas for scrolling
        self.left_canvas = tk.Canvas(left_panel_outer, bg="#b0b0b0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel_outer, orient="vertical", command=self.left_canvas.yview)
        
        self.left_panel = tk.Frame(self.left_canvas, bg="#b0b0b0")
        self.left_panel.bind(
            "<Configure>",
            lambda e: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))
        )
        
        self.left_canvas.create_window((0, 0), window=self.left_panel, anchor="nw")
        self.left_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.left_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scroll support
        def _on_mousewheel(event):
            self.left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.left_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.create_system_controls()
        self.create_imaging_controls()
        self.create_bottom_buttons()
        
        # Center - Main viewing area
        center_frame = tk.Frame(main_frame, bg="white")
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Top info bar
        info_frame = tk.Frame(center_frame, bg="#b0b0b0")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.sample_name_label = tk.Label(info_frame, text="Select a sample", 
                                          font=("Arial", 16, "bold"), bg="#b0b0b0")
        self.sample_name_label.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(info_frame, text="Chamber at atmosphere — evacuate to continue",
                                     font=("Arial", 10), fg="#555", bg="#b0b0b0")
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Button group top right
        buttons_frame = tk.Frame(center_frame, bg="white")
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(buttons_frame, text="Choose Sample", command=self.open_sample_selector,
                 bg="#1e3a5f", fg="white", padx=10, pady=5).pack(side=tk.RIGHT, padx=5)
        tk.Button(buttons_frame, text="Save", command=self.save_image,
                 bg="#1e3a5f", fg="white", padx=10, pady=5).pack(side=tk.RIGHT, padx=5)
        tk.Button(buttons_frame, text="Reset", command=self.reset_simulator,
                 bg="#1e3a5f", fg="white", padx=10, pady=5).pack(side=tk.RIGHT, padx=5)
        
        # Canvas for image display
        self.canvas = tk.Canvas(center_frame, bg="#000000", height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_system_controls(self):
        """Create system control section"""
        system_frame = tk.LabelFrame(self.left_panel, text="System", font=("Arial", 12, "bold"),
                                     bg="#b0b0b0", padx=15, pady=15)
        system_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Evacuate button
        self.evacuate_btn = tk.Button(system_frame, text="Evacuate", 
                                      command=self.evacuate_chamber,
                                      bg="#2e5f9f", fg="white", font=("Arial", 11, "bold"),
                                      padx=20, pady=10)
        self.evacuate_btn.pack(pady=10)
        
        # HV toggle
        hv_frame = tk.Frame(system_frame, bg="#b0b0b0")
        hv_frame.pack(fill=tk.X, pady=10)
        
        self.hv_var = tk.StringVar(value="OFF")
        self.hv_btn = tk.Button(hv_frame, text="HV OFF", command=self.toggle_hv,
                               bg="#8f3f3f", fg="white", font=("Arial", 10, "bold"),
                               padx=15, pady=5)
        self.hv_btn.pack()
        
        tk.Label(system_frame, text="Accelerating Voltage", font=("Arial", 9, "bold"),
                bg="#b0b0b0").pack(anchor="w", pady=(10, 0))
        
        voltage_frame = tk.Frame(system_frame, bg="#b0b0b0")
        voltage_frame.pack(fill=tk.X)
        
        self.voltage_var = tk.IntVar(value=10)
        voltage_combo = ttk.Combobox(voltage_frame, textvariable=self.voltage_var,
                                     values=[str(v) for v in self.voltage_options],
                                     state="readonly", width=10)
        voltage_combo.pack(anchor="w")
        voltage_combo.bind("<<ComboboxSelected>>", lambda *args: self.update_image())
        
        tk.Label(system_frame, text="Spot size", font=("Arial", 9, "bold"),
                bg="#b0b0b0").pack(anchor="w", pady=(10, 0))
        
        spot_frame = tk.Frame(system_frame, bg="#b0b0b0")
        spot_frame.pack(fill=tk.X)
        
        self.spot_var = tk.IntVar(value=5)
        spot_combo = ttk.Combobox(spot_frame, textvariable=self.spot_var,
                                  values=[str(v) for v in self.spot_size_options],
                                  state="readonly", width=10)
        spot_combo.pack(anchor="w")
        spot_combo.bind("<<ComboboxSelected>>", lambda *args: self.update_image())
        
        tk.Label(system_frame, text="Z height distance", font=("Arial", 9, "bold"),
                bg="#b0b0b0").pack(anchor="w", pady=(10, 0))
        
        height_frame = tk.Frame(system_frame, bg="#b0b0b0")
        height_frame.pack(fill=tk.X)
        
        self.height_var = tk.IntVar(value=10)
        height_combo = ttk.Combobox(height_frame, textvariable=self.height_var,
                                    values=[str(v) for v in self.height_options],
                                    state="readonly", width=10)
        height_combo.pack(anchor="w")
        height_combo.bind("<<ComboboxSelected>>", lambda *args: self.update_image())
    
    def create_imaging_controls(self):
        """Create imaging control section"""
        imaging_frame = tk.LabelFrame(self.left_panel, text="Imaging", font=("Arial", 12, "bold"),
                                      bg="#b0b0b0", padx=15, pady=15)
        imaging_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(imaging_frame, text="Brightness", font=("Arial", 9, "bold"),
                bg="#b0b0b0").pack(anchor="w", pady=(0, 5))
        
        self.brightness_var = tk.IntVar(value=100)
        brightness_scale = tk.Scale(imaging_frame, from_=50, to=150, orient=tk.HORIZONTAL,
                variable=self.brightness_var, bg="#9a9a9a", length=250,
                command=lambda *args: self.update_image())
        brightness_scale.pack(fill=tk.X)
        
        tk.Label(imaging_frame, text="Contrast", font=("Arial", 9, "bold"),
                bg="#b0b0b0").pack(anchor="w", pady=(10, 5))
        
        self.contrast_var = tk.IntVar(value=100)
        contrast_scale = tk.Scale(imaging_frame, from_=50, to=150, orient=tk.HORIZONTAL,
                variable=self.contrast_var, bg="#9a9a9a", length=250,
                command=lambda *args: self.update_image())
        contrast_scale.pack(fill=tk.X)
        
        tk.Label(imaging_frame, text="Focus", font=("Arial", 9, "bold"),
                bg="#b0b0b0").pack(anchor="w", pady=(10, 5))
        
        self.focus_var = tk.IntVar(value=100)
        focus_scale = tk.Scale(imaging_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                variable=self.focus_var, bg="#9a9a9a", length=250,
                command=lambda *args: self.update_image())
        focus_scale.pack(fill=tk.X)
        
        tk.Label(imaging_frame, text="Magnification", font=("Arial", 9, "bold"),
                bg="#b0b0b0").pack(anchor="w", pady=(10, 5))
        
        self.magnification_var = tk.IntVar(value=1)
        magnif_scale = tk.Scale(imaging_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                               variable=self.magnification_var, bg="#9a9a9a", length=250,
                               command=lambda *args: self.update_image())
        magnif_scale.pack(fill=tk.X)
        
        self.magnif_label = tk.Label(imaging_frame, text="1x", bg="#b0b0b0")
        self.magnif_label.pack()
        
        self.magnification_var.trace("w", lambda *args: self.update_magnif_label())
    
    def create_bottom_buttons(self):
        """Create bottom control buttons"""
        button_frame = tk.Frame(self.left_panel, bg="#b0b0b0")
        button_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        tk.Button(button_frame, text="Import Image", command=self.import_image,
                 bg="#2e5f9f", fg="white", font=("Arial", 10, "bold"),
                 padx=15, pady=8).pack(fill=tk.X, pady=5)
    
    def evacuate_chamber(self):
        """Evacuate chamber - required before HV can turn on"""
        if not self.chamber_evacuated:
            self.chamber_evacuated = True
            self.evacuate_btn.config(state=tk.DISABLED, bg="#4a7f7f")
            self.status_label.config(text="Chamber evacuated — ready to enable HV")
            messagebox.showinfo("Success", "Chamber evacuated successfully!")
        else:
            messagebox.showwarning("Info", "Chamber already evacuated!")
    
    def toggle_hv(self):
        """Toggle HV - only works after chamber evacuation"""
        if not self.chamber_evacuated:
            messagebox.showerror("Error", "Evacuate chamber first!")
            return
        
        self.hv_on = not self.hv_on
        
        if self.hv_on:
            self.hv_btn.config(text="HV ON", bg="#2e8f2e")
            self.status_label.config(text="HV enabled — image now visible")
            if self.current_sample:
                self.update_image()
        else:
            self.hv_btn.config(text="HV OFF", bg="#8f3f3f")
            self.status_label.config(text="HV disabled — no image visible")
            self.canvas.delete("all")
            self.canvas.create_text(700, 400, text="HV OFF - No image", 
                                   fill="white", font=("Arial", 16))
    
    def open_sample_selector(self):
        """Open modal for sample selection"""
        selector = tk.Toplevel(self.root)
        selector.title("Select a sample to explore")
        selector.geometry("700x400")
        selector.configure(bg="white")
        
        title = tk.Label(selector, text="Select a sample to explore", 
                        font=("Arial", 14, "bold"), bg="white")
        title.pack(pady=15)
        
        # Category buttons
        category_frame = tk.Frame(selector, bg="white")
        category_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.current_category = None
        self.category_buttons = {}
        
        def select_category(cat):
            self.current_category = cat
            for btn, category in self.category_buttons.items():
                if category == cat:
                    btn.config(relief=tk.SUNKEN, bg="#1e3a5f", fg="white")
                else:
                    btn.config(relief=tk.RAISED, bg="#d0d0d0", fg="black")
            display_samples(cat)
        
        for category in self.samples.keys():
            btn = tk.Button(category_frame, text=category, 
                           command=lambda c=category: select_category(c),
                           bg="#d0d0d0", padx=10, pady=5)
            btn.pack(side=tk.LEFT, padx=5)
            self.category_buttons[btn] = category
        
        # Sample display
        sample_frame = tk.Frame(selector, bg="white")
        sample_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.sample_buttons = {}
        
        def display_samples(category):
            for widget in sample_frame.winfo_children():
                widget.destroy()
            
            for sample in self.samples[category]:
                btn = tk.Button(sample_frame, text=sample, 
                              command=lambda s=sample: choose_sample(s),
                              bg="#f0f0f0", padx=15, pady=10, width=20)
                btn.pack(pady=5)
        
        def choose_sample(sample):
            self.current_sample = sample
            self.sample_name_label.config(text=sample)
            self.status_label.config(text="Sample loaded — ready to observe")
            if self.hv_on:
                self.update_image()
            selector.destroy()
        
        # Select first category by default
        first_category = list(self.samples.keys())[0]
        select_category(first_category)
    
    def update_image(self):
        """Update image with all adjustments - realistic SEM parameter effects"""
        if not self.hv_on:
            self.canvas.delete("all")
            self.canvas.create_text(700, 400, text="Turn on HV to view image",
                                   fill="white", font=("Arial", 16))
            return
        
        if not self.current_sample or self.current_sample not in self.sample_images:
            return
        
        image_path = self.sample_images[self.current_sample]
        
        if not os.path.exists(image_path):
            self.canvas.delete("all")
            self.canvas.create_text(700, 400, text=f"Image not found: {image_path}",
                                   fill="red", font=("Arial", 12))
            return
        
        # Load image
        try:
            img = Image.open(image_path).convert("RGB")
            
            # Apply magnification with improved scaling
            magnification = self.magnification_var.get()
            base_size = min(img.width, img.height)
            
            if magnification > 1:
                # For higher magnifications, we first resize the image larger
                # then crop the center portion to simulate zooming in
                zoom_size = int(base_size * magnification)
                img = img.resize((zoom_size, zoom_size), Image.Resampling.LANCZOS)
                
                # Calculate the center region to crop
                crop_size = base_size
                left = (zoom_size - crop_size) // 2
                top = (zoom_size - crop_size) // 2
                right = left + crop_size
                bottom = top + crop_size
                
                # Crop to center region for magnification effect
                img = img.crop((left, top, right, bottom))
                
                # Apply additional sharpening for higher magnifications
                # Increase sharpness progressively with magnification
                sharpness_factor = 1.0 + (magnification * 0.1)  # Gradually increase sharpness
                img = ImageEnhance.Sharpness(img).enhance(sharpness_factor)
            
            # Apply Z height defocus blur
            height = self.height_var.get()
            optimal_height = 10
            focus_blur = abs(height - optimal_height) * 0.8
            if focus_blur > 0.1:
                img = img.filter(ImageFilter.GaussianBlur(radius=focus_blur))
            
            # Apply spot size blur
            spot_size = self.spot_var.get()
            spot_blur = (21 - spot_size) * 0.4
            if spot_blur > 0.1:
                img = img.filter(ImageFilter.GaussianBlur(radius=spot_blur))
            
            # Apply voltage-dependent contrast
            voltage = self.voltage_var.get()
            voltage_contrast = 0.7 + (voltage / 30.0) * 0.6
            img = ImageEnhance.Contrast(img).enhance(voltage_contrast)
            
            # Apply manual focus adjustment
            focus_value = self.focus_var.get()
            if focus_value < 100:
                focus_blur_manual = (100 - focus_value) * 0.2
                if focus_blur_manual > 0.1:
                    img = img.filter(ImageFilter.GaussianBlur(radius=focus_blur_manual))
            
            # Apply brightness
            brightness = self.brightness_var.get() / 100.0
            img = ImageEnhance.Brightness(img).enhance(brightness)
            
            # Apply contrast
            contrast = self.contrast_var.get() / 100.0
            img = ImageEnhance.Contrast(img).enhance(contrast)
            
            # Resize to fit canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width < 2 or canvas_height < 2:
                canvas_width = 1000
                canvas_height = 600
            
            img.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
            
            # Store for saving
            self.current_image_pil = img
            
            # Display
            photo = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, 
                                    image=photo)
            self.canvas.image = photo
            
        except Exception as e:
            self.canvas.delete("all")
            self.canvas.create_text(700, 400, text=f"Error loading image: {str(e)}",
                                   fill="red", font=("Arial", 12))
    
    def update_magnif_label(self):
        """Update magnification display"""
        magnif = self.magnification_var.get()
        self.magnif_label.config(text=f"{magnif}x")
    
    def update_status(self):
        """Update status based on state"""
        if not self.chamber_evacuated:
            self.status_label.config(text="Chamber at atmosphere — evacuate to continue")
        elif not self.hv_on:
            self.status_label.config(text="Chamber evacuated — ready to enable HV")
        else:
            self.status_label.config(text="HV enabled — image now visible")
    
    def save_image(self):
        """Save current image"""
        if self.current_image_pil is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        
        if file_path:
            self.current_image_pil.save(file_path)
            messagebox.showinfo("Success", f"Image saved to {file_path}")
    
    def import_image(self):
        """Import custom image"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.png *.bmp *.tiff")]
        )
        
        if file_path:
            self.current_sample = os.path.basename(file_path)
            self.sample_name_label.config(text=self.current_sample)
            self.sample_images[self.current_sample] = file_path
            
            if self.hv_on:
                self.update_image()
            else:
                messagebox.showinfo("Info", "Turn on HV to view the imported image")
    
    def reset_simulator(self):
        """Reset simulator to initial state"""
        self.chamber_evacuated = False
        self.hv_on = False
        self.current_sample = None
        
        self.evacuate_btn.config(state=tk.NORMAL, bg="#2e5f9f")
        self.hv_btn.config(text="HV OFF", bg="#8f3f3f")
        self.sample_name_label.config(text="Select a sample")
        self.status_label.config(text="Chamber at atmosphere — evacuate to continue")
        
        self.brightness_var.set(100)
        self.contrast_var.set(100)
        self.focus_var.set(100)
        self.magnification_var.set(1)
        self.voltage_var.set(10)
        self.spot_var.set(5)
        self.height_var.set(10)
        
        self.canvas.delete("all")
        messagebox.showinfo("Success", "Simulator reset to initial state")

def main():
    root = tk.Tk()
    app = SEMSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
