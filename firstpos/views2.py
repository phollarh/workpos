


class SalesRcListsView(LoginRequiredMixin, View):
	@method_decorator(login_required, name='dispatch')
	@method_decorator(email_verified_required, name='dispatch')
	def get(self, *args, **kwargs):
		start_date_str = self.request.GET.get('start_date')
		end_date_str = self.request.GET.get('end_date')

		start_date = timezone.now().date() if not start_date_str else timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
		end_date = timezone.now().date() if not end_date_str else timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()

		if not start_date_str and not end_date_str:
			Receipts = SalesReceipt.objects.filter(
				user=self.request.user, 
				issued=True
				).order_by('-date')

			p=Paginator(Receipts, 1)

	

			page = self.request.GET.get('page')


		

			try :

				Receipt= p.page(page)
			except PageNotAnInteger :

				Receipt = p.page(1)

			except EmptyPage :
				Receipt = p.page(p.num_pages) if p.num_pages > 0 else p.page(1)
			number_of_pages = p.get_elided_page_range()

			if Receipt.number <= 10:
				number_of_pages = range(1, min(11, Receipt.paginator.num_pages + 1))
			elif Receipt.number > Receipt.paginator.num_pages - 10 :
				number_of_pages = range(Receipt.paginator.num_pages - 10, Receipt.paginator.num_pages + 1)
			else:
				number_of_pages = range(Receipt.number - 5, Receipt.number + 5)

	        # Add ellipsis if necessary
			#if number_of_pages[0] != "1":
			#	number_of_pages.insert(0, "...")
			#if number_of_pages[-1] != str(Receipt.paginator.num_pages):
			#	number_of_pages.append("...")
			context = {
            "start_date": start_date,
            "end_date": end_date,
            "Receipt": Receipt,
            "number_of_pages": number_of_pages,
    	    }

        # Pass the filter parameters in the context to include them in the pagination links
			context.update(self.request.GET.dict())


		else:
			Receipts = SalesReceipt.objects.filter(
                user=self.request.user,
                issued=True,
                date__date__gte=start_date,
                date__date__lte=end_date
            ).order_by('-date')

			p=Paginator(Receipts, 1)

	

			page = self.request.GET.get('page')


		

			try :

				Receipt= p.page(page)
			except PageNotAnInteger :

				Receipt = p.page(1)

			except EmptyPage :
				Receipt = p.page(p.num_pages) if p.num_pages > 0 else p.page(1)
			number_of_pages = p.get_elided_page_range()

			if Receipt.number <= 10:
				number_of_pages = range(1, min(11, Receipt.paginator.num_pages + 1))
			elif Receipts.number > Receipt.paginator.num_pages - 10 :
				number_of_pages = range(Receipt.paginator.num_pages - 10, Receipt.paginator.num_pages + 1)
			else:
				number_of_pages = range(Receipt.number - 5, Receipt.number + 5)
			context = {
            "start_date": start_date,
            "end_date": end_date,
            "Receipt": Receipt,
            "number_of_pages": number_of_pages,
    	    }

        # Pass the filter parameters in the context to include them in the pagination links
			context.update(self.request.GET.dict())

		return render(self.request, 'salesrc.html', context)

