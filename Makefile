gnuplot_files = plot
python_files = Rep_Rotation Geodesic_Parameters Control_Curves Controls Errors Geodesic_Curves Implementation Test_Scenarios
plot_files = Plot_Angles Plot_Control_Curves Plot_Controls Plot_Errors Plot_Geodesics Plot_Parameters Plot_Random_Errors Plot_Sites_Errors


plot_all: clean $(gnuplot_files)
	bash plot_names.sh

all: $(python_files) $(plot_files)

$(python_files): %:
	python3 $@.py

$(gnuplot_files): %:
	gnuplot $@.gp

$(plot_files): %:
	python3 $@.py

clean:
	rm -rf Figures
	mkdir Figures
